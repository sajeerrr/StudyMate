import streamlit as st
import requests

st.title("Upload PDF")

uploaded_file = st.file_uploader(
    "Choose PDF",
    type=["pdf"]
)

if uploaded_file:
    files = {
        "files":(
            uploaded_file.name,
            uploaded_file,
            "application/pdf"
            )
    }

    response = requests.post(
        "http://localhost:8000/upload",
        files=files
    )

    st.success(
        response.json()["message"]
    )