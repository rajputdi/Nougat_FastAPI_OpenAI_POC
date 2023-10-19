import tiktoken


def get_metadata(text):
    prompt = f"Please summarize the following text so that a teenager can understand what is written:\n\n{text}"
    encoding = tiktoken.encoding_for_model("text-davinci-002")
    num_tokens = len(encoding.encode(prompt))

    # Splitting text by whitespace to count words
    num_words = len(text.split())

    # Calculating the cost of the query based on the number of tokens
    cost = (num_tokens / 1000) * 0.0060

    return {
        "Model": "text-davinci-002",
        "Encoding Name": "p50k_base",
        "Number of Tokens": num_tokens,
        "Number of Words": num_words,
        "Cost of Query ($)": cost,
    }
