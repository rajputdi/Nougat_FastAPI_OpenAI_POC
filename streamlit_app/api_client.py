import requests
from requests.exceptions import RequestException


def extract_text(url, library, nougat_api_address=None):
    api_url = "https://damg7245-asng2-team4-fd9f8dd6d40f.herokuapp.com/extract-text"  # Update the address if your FastAPI service is hosted elsewhere
    data = {"url": url, "library": library, "nougat_api_address": nougat_api_address}
    response = requests.post(api_url, json=data)
    if response.status_code != 200:
        return (
            response.json(),
            response.status_code,
        )  # Return both data and status code for non-200 responses
    response.raise_for_status()  # This will raise an exception for bad responses (other than 400)
    return response.json(), response.status_code  # Return both data and status code


def generate_summary(text):
    api_url = "https://damg7245-asng2-team4-fd9f8dd6d40f.herokuapp.com/generate-summary"
    data = {"text": text}
    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()  # This will raise an exception for bad responses
        return response.json(), response.status_code
    except RequestException as e:
        print(f"An error occurred: {e}")
        return None, response.status_code if response else None


def ask_question(extracted_text, question):
    api_url = "https://damg7245-asng2-team4-fd9f8dd6d40f.herokuapp.com/ask-question"
    data = {"extracted_text": extracted_text, "question": question}
    response = requests.post(api_url, json=data)
    if response.status_code != 200:
        return response.json(), response.status_code
    response.raise_for_status()
    return response.json(), response.status_code
