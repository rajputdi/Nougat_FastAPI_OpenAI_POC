import openai  # Assuming you are using the openai library
import os


async def get_summary(text):
    # Construct a prompt for summarization
    openai_api_key = os.environ["OPENAI_API_KEY"]
    openai.api_key = openai_api_key

    prompt = f"Please summarize within 250 words the following text that is extracted from a form related to regulation or policies from US Security and Exchange Commission website: \n\n{text}"

    # Use the OpenAI API to get the summary
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=300,
    )

    return response.choices[0].text.strip()
