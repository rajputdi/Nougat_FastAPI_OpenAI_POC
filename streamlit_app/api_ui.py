# # import streamlit as st
# # import requests
# # from fastapi import FastAPI, HTTPException, Request
# # from requests.exceptions import RequestException
# # from api_client import extract_text

# # st.title("PDF Text Extraction App")

# # pdf_url = st.text_input("Enter PDF URL:")
# # library_choice = st.selectbox("Choose Library:", options=["pypdf", "nougat"])
# # api_address = st.text_input(
# #     "API URL (If using Nougat)", "", placeholder="Connect to API for GPU computation"
# # )


# # if st.button("Extract Text"):
# #     if pdf_url:
# #         try:
# #             response_data = extract_text(pdf_url, library_choice)
# #             st.write("Extracted Text:")
# #             st.write(response_data.get("text", "No text extracted"))
# #         except requests.RequestException as e:
# #             st.error(f"An error occurred: {str(e)}")
# #     else:
# #         st.error("Please enter a PDF URL")


# import streamlit as st
# from api_client import (
#     extract_text,
# )  # Ensure this import is correct based on your file structure

# st.title("PDF Text Extraction App")

# pdf_url = st.text_input("Enter PDF URL:")
# library_choice = st.selectbox(
#     "Choose Library:", options=["pypdf", "nougat"]
# )  # Added "nougat" option
# nougat_api_address = (
#     st.text_input("Enter Nougat API Address:") if library_choice == "nougat" else None
# )

# if st.button("Extract Text"):
#     if pdf_url:
#         try:
#             response_data = extract_text(pdf_url, library_choice, nougat_api_address)
#             st.write("Extracted Text:")
#             st.write(response_data.get("text", "No text extracted"))
#         except requests.RequestException as e:
#             st.error(f"An error occurred: {str(e)}")
#     else:
#         st.error("Please enter a PDF URL")

# # Ensure the correct import for requests exceptions
# import requests
# from requests.exceptions import RequestException


# import streamlit as st
# from api_client import (
#     extract_text,
# )  # Ensure this import is correct based on your file structure
# import requests
# from requests.exceptions import RequestException

# st.title("PDF Text Extraction App")

# pdf_url = st.text_input("Enter PDF URL:")
# library_choice = st.selectbox(
#     "Choose Library:", options=["pypdf", "nougat"]
# )  # Added "nougat" option
# nougat_api_address = (
#     st.text_input("Enter Nougat API Address:") if library_choice == "nougat" else None
# )

# if st.button("Extract Text"):
#     if pdf_url:
#         try:
#             response_data = extract_text(pdf_url, library_choice, nougat_api_address)
#             st.write("Extracted Text:")
#             st.write(response_data.get("text", "No text extracted"))
#         except RequestException as e:
#             st.error(f"An error occurred: {str(e)}")
#     else:
#         st.error("Please enter a PDF URL")


import streamlit as st
from api_client import (
    extract_text,
    generate_summary,
)  # Ensure this import is correct based on your file structure
import requests
from requests.exceptions import RequestException

st.title("Nougat v/s PyPdf, Q/A Model-OpenAI")

pdf_url = st.text_input("Enter PDF URL:")
library_choice = st.selectbox(
    "Choose Library:", options=["pypdf", "nougat"]
)  # Added "nougat" option
nougat_api_address = (
    st.text_input("Enter Nougat API Address:") if library_choice == "nougat" else None
)

if st.button("Extract Text"):
    if pdf_url:
        try:
            response_data, status_code = extract_text(
                pdf_url, library_choice, nougat_api_address
            )  # Assuming extract_text returns both data and status code
            if status_code == 200:
                extracted_text = response_data.get("text", "No text extracted")
                st.write("Extracted Text:")
                # st.write(response_data.get("text", "No text extracted"))
                st.text_area(
                    "Text: ",
                    value=response_data.get("text", "No text extracted").strip(),
                    height=400,
                )
            elif status_code == 400:
                st.error(
                    response_data.get("detail", "An unexpected error occurred.")
                )  # Display custom error message from API
            else:
                st.error(f"An error occurred: {status_code}")
        except RequestException as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter a PDF URL")


if st.button("Generate Summary"):
    if extracted_text:  # Assuming extracted_text holds the text extracted from PDF
        summary_response_data, summary_status_code = generate_summary(
            extracted_text
        )  # Assuming generate_summary is your client function to call the new endpoint
        if summary_status_code == 200:
            st.write("Summary:")
            st.write(summary_response_data.get("summary", "No summary generated"))
        else:
            st.error(f"An error occurred: {summary_status_code}")
