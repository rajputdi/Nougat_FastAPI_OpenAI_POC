from fastapi import FastAPI, HTTPException, Request
import requests
from PyPDF2 import PdfFileReader
from io import BytesIO

app = FastAPI()


@app.post("/extract-text/")
async def extract_text(request: Request):
    data = await request.json()
    url = data.get("url")
    library_choice = data.get("library")

    # Validate the URL and library choice
    if not url or not library_choice:
        raise HTTPException(status_code=400, detail="Invalid input")

    # Fetch the PDF
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to retrieve PDF")

    pdf_bytes = BytesIO(response.content)

    # Extract text using PyPDF2 (Nougat can be added in a similar way)
    if library_choice == "pypdf":
        pdf_reader = PdfFileReader(pdf_bytes)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    else:
        raise HTTPException(status_code=400, detail="Invalid library choice")

    return {"text": text}
