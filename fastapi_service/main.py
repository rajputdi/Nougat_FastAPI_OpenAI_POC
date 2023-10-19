# from fastapi import FastAPI, HTTPException, Request
# from pdf_extractor import (
#     fetch_pdf,
#     extract_text_pypdf,
#     extract_text_nougat,
# )  # Import the necessary functions
# import requests
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )


# @app.post("/extract-text/")
# async def extract_text(request: Request):
#     data = await request.json()
#     url = data.get("url")
#     library_choice = data.get("library")
#     nougat_api_address = data.get(
#         "nougat_api_address"
#     )  # Get the Nougat API address from the request data

#     # Validate the URL and library choice
#     if not url or not library_choice:
#         raise HTTPException(status_code=400, detail="Invalid input")

#     if library_choice == "pypdf":
#         try:
#             pdf_bytes = fetch_pdf(url)
#             text = extract_text_pypdf(pdf_bytes)
#         except requests.RequestException:
#             raise HTTPException(status_code=400, detail="Failed to retrieve PDF")
#     elif library_choice == "nougat" and nougat_api_address:
#         text = extract_text_nougat(url, nougat_api_address)
#     else:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid library choice or missing Nougat API address",
#         )

#     return {"text": text}


from fastapi import FastAPI, HTTPException, Request, status
from pdf_extractor import (
    fetch_pdf,
    extract_text_pypdf,
    extract_text_nougat,
)  # Import the necessary functions
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


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
        text = extract_text_nougat(url, nougat_api_address)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid library choice or missing Nougat API address",
        )

    return {"text": text}
