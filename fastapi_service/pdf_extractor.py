import requests
import PyPDF2
from io import BytesIO


def fetch_pdf(url):
    response = requests.get(url)
    response.raise_for_status()  # This will raise an exception for bad responses
    return response.content


def extract_text_pypdf(pdf_bytes):
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


def extract_text_nougat(pdf_url, api_address):
    def parse_pdf_with_nougat(file_address, api_address):
        url = api_address + "/predict/"
        payload = {}
        pdf_response = requests.get(file_address)
        if pdf_response.status_code != 200:
            print(
                f"Failed to download PDF from {file_address}. Status code: {pdf_response.status_code}"
            )
            return None

        # Extract the PDF content
        pdf_content = pdf_response.content

        files = [("file", ("filefromweb.pdf", pdf_content, "application/pdf"))]

        headers = {}
        try:
            response = requests.request(
                "POST", url, headers=headers, data=payload, files=files
            )

            response.raise_for_status()
            content = response.text
            return content

        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")
            return None

    # Call your function and return the result
    return parse_pdf_with_nougat(pdf_url, api_address)
