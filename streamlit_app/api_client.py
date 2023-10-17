import requests


def extract_text(url, library, nougat_api_address=None):
    api_url = "http://127.0.0.1:8000/extract-text/"  # Update the address if your FastAPI service is hosted elsewhere
    data = {"url": url, "library": library, "nougat_api_address": nougat_api_address}
    response = requests.post(api_url, json=data)
    response.raise_for_status()  # This will raise an exception for bad responses
    return response.json()
