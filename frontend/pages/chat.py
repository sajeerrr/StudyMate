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