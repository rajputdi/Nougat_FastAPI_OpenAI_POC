# import requests


# def extract_text(url, library, nougat_api_address=None):
#     api_url = "https://damg7245-asng2-team4-fd9f8dd6d40f.herokuapp.com/extract-text"  # Update the address if your FastAPI service is hosted elsewhere
#     data = {"url": url, "library": library, "nougat_api_address": nougat_api_address}
#     response = requests.post(api_url, json=data)
#     response.raise_for_status()  # This will raise an exception for bad responses
#     return response.json()


import requests


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
