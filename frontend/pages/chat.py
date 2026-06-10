import streamlit as st
import requests

st.title("ChatBot")

question = st.text_input("Ask a Question")

if st.button("Ask"):
    response = requests.post(
        "http://localhost:8000/chat",
        json={
            "question": question
        }
    )

    st.write(response.json()["answer"])

# st.set_page_config(
#     page_title="StudyMate",
#     layout="wide"
# )

# st.title("StudyMate")

# st.sidebar.tile("Documents")

# uploaded_file = st.sidebar.file_uploader(
#     "Upload PDF",
#     type=["pdf"]
# )