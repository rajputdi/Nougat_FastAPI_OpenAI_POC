import openai  # Assuming you are using the openai library
import os


async def get_summary(text):
    # response = openai.Completion.create(
    #   engine="text-davinci-002",
    #   prompt=text,
    #   max_tokens=150  # You can adjust this value as needed
    # )
    # summary = response['choices'][0]['text'].strip()
    # return summary

    # Construct a prompt for summarization
    openai_api_key = os.environ["OPENAI_API_KEY"]
    openai.api_key = openai_api_key
    prompt = f"Please summarize the following text so that a teenager can understand what is written:\n\n{text}"

    # Use the OpenAI API to get the summary
    response = openai.Completion.create(
        model="text-davinci-002",  # You can choose other models like "gpt-3.5-turbo" based on your preference and API cost.
        prompt=prompt,
        max_tokens=150,  # Adjust based on how long you want the summary to be
    )

    return response.choices[0].text.strip()
