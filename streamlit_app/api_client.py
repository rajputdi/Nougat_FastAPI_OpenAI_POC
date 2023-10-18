import requests


def extract_text(url, library, nougat_api_address=None):
    api_url = "https://damg7245-asng2-team4-fd9f8dd6d40f.herokuapp.com/"  # Update the address if your FastAPI service is hosted elsewhere
    data = {"url": url, "library": library, "nougat_api_address": nougat_api_address}
    response = requests.post(api_url, json=data)
    response.raise_for_status()  # This will raise an exception for bad responses
    return response.json()
