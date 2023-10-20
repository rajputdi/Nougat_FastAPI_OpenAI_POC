import streamlit as st
from api_client import (
    extract_text,
    generate_summary,
    ask_question,
)  # Ensure this import is correct based on your file structure
from metadata import get_metadata
import requests
from requests.exceptions import RequestException

st.title("Nougat v/s PyPdf, Q/A Model-OpenAI")

# st.image("images/img_homescreen.png", caption="Looking for answers!")

image_url = "https://raw.githubusercontent.com/rajputdi/Nougat_FastAPI_OpenAI_POC/main/images/img_homescreen.png"

st.markdown(
    f'<p align="center"><img src="{image_url}" alt="looking for answers"></p>',
    unsafe_allow_html=True,
)


pdf_url = st.text_input("Enter PDF URL:")
library_choice = st.selectbox(
    "Choose Library:", options=["pypdf", "nougat"]
)  # Added "nougat" option
nougat_api_address = (
    st.text_input("Enter Nougat API Address:") if library_choice == "nougat" else None
)

if "extracted_text" not in st.session_state:
    st.session_state[
        "extracted_text"
    ] = None  # Initialize extracted_text in session_state

if st.button("Extract Text"):
    if pdf_url:
        try:
            response_data, status_code = extract_text(
                pdf_url, library_choice, nougat_api_address
            )  # Assuming extract_text returns both data and status code
            if status_code == 200:
                st.session_state["extracted_text"] = response_data.get(
                    "text", "No text extracted"
                )
                st.write("Extracted Text:")
                st.text_area(
                    "Text: ",
                    value=st.session_state["extracted_text"].strip(),
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

if st.button("Display Metadata"):
    if pdf_url and (
        st.session_state["extracted_text"]
        and st.session_state["extracted_text"].strip()
    ):
        metadata = get_metadata(st.session_state["extracted_text"])
        for key, value in metadata.items():
            st.write(f"{key}: {value}")
    else:
        st.error("No text available to generate metadata. Please extract text first.")


if st.button("Generate Summary"):
    if (
        st.session_state["extracted_text"]
        and st.session_state["extracted_text"].strip()
    ):
        summary_response_data, summary_status_code = generate_summary(
            st.session_state["extracted_text"]
        )
        if summary_status_code == 200:
            st.write("Summary:")
            st.write(summary_response_data.get("summary", "No summary generated"))
        else:
            st.error(f"An error occurred: {summary_status_code}")
    else:
        st.error("No text available to generate summary. Please extract text first.")


question = st.text_input("Enter your question:")
# st.write(st.session_state["extracted_text"])
if st.button("Ask Question"):
    if st.session_state["extracted_text"] and question:
        answer_data, answer_status_code = ask_question(
            st.session_state["extracted_text"], question
        )
        if answer_status_code == 200:
            st.write("Answer:")
            st.write(answer_data.get("answer", "No answer provided"))
        else:
            st.error(f"An error occurred (UI): {answer_status_code}")
    else:
        st.error(
            "No text available or question provided. Please extract text and enter a question first."
        )
