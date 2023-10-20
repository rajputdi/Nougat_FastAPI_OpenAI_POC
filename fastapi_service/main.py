from fastapi import FastAPI, HTTPException, Request, status
from pdf_extractor import (
    fetch_pdf,
    extract_text_pypdf,
    extract_text_nougat,
)  # Import the necessary functions
from summary import get_summary
from search_j import get_text
import requests
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlparse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


@app.post("/extract-text/")
async def extract_text(request: Request):
    data = await request.json()
    url = data.get("url")
    library_choice = data.get("library")
    nougat_api_address = data.get(
        "nougat_api_address"
    )  # Get the Nougat API address from the request data

    # Validate the URL and library choice
    if not url or not library_choice:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input"
        )

    if library_choice == "pypdf":
        try:
            pdf_bytes = fetch_pdf(url)
            text = extract_text_pypdf(pdf_bytes)
        except requests.RequestException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve PDF"
            )
    elif library_choice == "nougat" and nougat_api_address:
        if not is_valid_url(nougat_api_address):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Nougat API address",
            )
        text = extract_text_nougat(url, nougat_api_address)
        if text is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The entered Nougat API address is incorrect, as a result extracted text is None",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid library choice or missing Nougat API address",
        )

    return {"text": text}


# CHG10192023_DR
@app.post("/generate-summary/")
async def generate_summary(request: Request):
    data = await request.json()
    text = data.get("text")

    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No text provided"
        )

    # Call OpenAI API to generate summary
    summary = await get_summary(
        text
    )  # Assuming get_summary is your function to call OpenAI API
    return {"summary": summary}


@app.post("/ask-question/")
async def ask_question(request: Request):
    data = await request.json()
    extracted_text = data.get("extracted_text")
    question = data.get("question")

    if not extracted_text or not question:
        raise HTTPException(status_code=400, detail="Invalid input")

    # Assume `get_answer` is a function that sends the question and text to OpenAI
    answer = await get_text(extracted_text, question)
    return {"answer": answer}
