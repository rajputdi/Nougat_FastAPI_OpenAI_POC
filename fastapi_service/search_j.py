import openai  # for generating embeddings
import pandas as pd  # for DataFrames to store article sections and embeddings
import re  # for cutting <ref> links out of Wikipedia articles
import tiktoken  # for counting tokens
import ast  # for converting embeddings saved as strings back to arrays
from scipy import spatial  # for calculating vector similarities for search
import os

GPT_MODEL = "gpt-3.5-turbo"  # only matters insofar as it selects which tokenizer to use
openai_api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = openai_api_key
EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def halved_by_delimiter(string: str, delimiter: str = "\n") -> list[str, str]:
    """Split a string in two, on a delimiter, trying to balance tokens on each side."""
    chunks = string.split(delimiter)
    if len(chunks) == 1:
        return [string, ""]  # no delimiter found
    elif len(chunks) == 2:
        return chunks  # no need to search for halfway point
    else:
        total_tokens = num_tokens(string)
        halfway = total_tokens // 2
        best_diff = halfway
        for i, chunk in enumerate(chunks):
            left = delimiter.join(chunks[: i + 1])
            left_tokens = num_tokens(left)
            diff = abs(halfway - left_tokens)
            if diff >= best_diff:
                break
            else:
                best_diff = diff
        left = delimiter.join(chunks[:i])
        right = delimiter.join(chunks[i:])
        return [left, right]


def truncated_string(
    string: str,
    model: str,
    max_tokens: int,
    print_warning: bool = True,
) -> str:
    """Truncate a string to a maximum number of tokens."""
    encoding = tiktoken.encoding_for_model(model)
    encoded_string = encoding.encode(string)
    truncated_string = encoding.decode(encoded_string[:max_tokens])
    if print_warning and len(encoded_string) > max_tokens:
        print(
            f"Warning: Truncated string from {len(encoded_string)} tokens to {max_tokens} tokens."
        )
    return truncated_string


def split_strings_from_subsection(
    subsection: list,
    max_tokens: int = 1000,
    model: str = GPT_MODEL,
    max_recursion: int = 5,
) -> list[str]:
    """
    Split a subsection into a list of subsections, each with no more than max_tokens.
    Each subsection is a tuple of parent titles [H1, H2, ...] and text (str).
    """
    # titles, text = subsection
    string = subsection
    num_tokens_in_string = num_tokens(string)
    # if length is fine, return string
    if num_tokens_in_string <= max_tokens:
        return [string]
    # if recursion hasn't found a split after X iterations, just truncate
    elif max_recursion == 0:
        return [truncated_string(string, model=model, max_tokens=max_tokens)]
    # otherwise, split in half and recurse
    else:
        text = subsection
        for delimiter in ["\n\n", "\n", ". "]:
            left, right = halved_by_delimiter(text, delimiter=delimiter)
            if left == "" or right == "":
                # if either half is empty, retry with a more fine-grained delimiter
                continue
            else:
                # recurse on each half
                results = []
                for half in [left, right]:
                    half_subsection = half
                    half_strings = split_strings_from_subsection(
                        half_subsection,
                        max_tokens=max_tokens,
                        model=model,
                        max_recursion=max_recursion - 1,
                    )
                    results.extend(half_strings)
                return results
    # otherwise no split was found, so just truncate (should be very rare)
    return [truncated_string(string, model=model, max_tokens=max_tokens)]


def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100,
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]


def query_message(query: str, df: pd.DataFrame, model: str, token_budget: int) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = 'Use the form to answer the subsequent question. If the answer cannot be found in the form, write "I could not find an answer."'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'"""\n{string}\n"""'
        if num_tokens(message + next_article + question, model=model) > token_budget:
            break
        else:
            message += next_article
    return message + question


def ask(
    query: str,
    df: pd.DataFrame,
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 500,
    print_message: bool = False,
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": "You answer questions about Sec Forms."},
        {"role": "user", "content": message},
    ]
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=0
    )
    response_message = response["choices"][0]["message"]["content"]
    return response_message


async def get_text(text, question):
    list_string = text.split("\n")
    strings_list = []
    temp = ""
    for i, string in enumerate(list_string):
        if i % 9 != 0:
            temp += string
        else:
            temp += string
            strings_list.append("".join(temp))

    MAX_TOKENS = 1600
    strings = []
    for section in strings_list:
        strings.extend(split_strings_from_subsection(section, max_tokens=MAX_TOKENS))

    # print(f"{len(strings_list)} Wikipedia sections split into {len(strings)} strings.")

    tokens_count = []
    for string in strings:
        tokens_count.append(num_tokens(string))

    # len(tokens_count)

    df = pd.DataFrame({"Content": strings, "Tokens": tokens_count})

    # calculate embeddings
    BATCH_SIZE = 1000  # you can submit up to 2048 embedding inputs per request

    embeddings = []
    for batch_start in range(0, len(strings), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = strings[batch_start:batch_end]
        print(f"Batch {batch_start} to {batch_end-1}")
        response = openai.Embedding.create(model=EMBEDDING_MODEL, input=batch)
        for i, be in enumerate(response["data"]):
            assert (
                i == be["index"]
            )  # double check embeddings are in same order as input
        batch_embeddings = [e["embedding"] for e in response["data"]]
        embeddings.extend(batch_embeddings)

    df = pd.DataFrame({"text": strings, "embedding": embeddings})

    def list_to_string(lst):
        string_list = [str(l) for l in lst]
        return ", ".join(string_list)  # You can customize the separator as needed

    # Apply the custom function to the specific column
    df["embedding"] = df["embedding"].apply(list_to_string)

    # df['embedding'] = list(df['embedding'])
    df["embedding"] = df["embedding"].apply(ast.literal_eval)

    answer = ask(question, df=df)

    return answer
