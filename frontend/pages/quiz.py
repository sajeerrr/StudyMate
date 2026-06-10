import streamlit as st
import requests

topic = st.text_input("Topic")

difficulty = st.selectbox(
    "Difficulty",["Easy","Medium","Hard"]
)

if st.button("Generate Quiz"):
    response = requests.post(
        "http://localhost:8000/quiz",
        json={
            "topic": topic,
            "difficulty": difficulty,
            "num_questions": 5
        }
    )

    quiz = response.json()

    st.json(quiz)