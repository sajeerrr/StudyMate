import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_answer(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        message=[
            {
                "role":"user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content