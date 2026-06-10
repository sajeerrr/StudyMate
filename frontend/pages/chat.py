import streamlit as st
import requests

# st.title("ChatBot")

# question = st.text_input("Ask a Question")

# if st.button("Ask"):
#     response = requests.post(
#         "http://localhost:8000/chat",
#         json={
#             "question": question
#         }
#     )

#     st.write(response.json()["answer"])

st.set_page_config(
    page_title="StudyMate",
    layout="wide"
)

st.title("StudyMate")

#sidebar
st.sidebar.title("Documents")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    if st.sidebar.button("Upload"):
        files = {
            "file":(
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        with st.sidebar:
            with st.spinner("Processing PDF..."):
                response = requests.post(
                    "http://localhost:8000/upload",
                    files=files
                )

        st.sidebar.success(
            response.json()["message"]
        )
        st.session_state["upload_success"] = True
        st.rerun()

#Document list in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Uploaded Documents")

try:
    docs = requests.get(
        "http://localhost:8000/files"
    ).json()

    for doc in docs:
        col1, col2 = st.sidebar.columns([4, 1])

        with col1:
            st.write(doc["name"])
        with col2:
            if st.button("🗑️",key=doc["file_id"]):
                requests.delete(
                    f"http://localhost:8000/pdf/{doc['file_id']}"
                )
                st.rerun()
# except:
#     st.sidebar.info("No documents uploaded")
except Exception as e:
    st.sidebar.error(str(e))


#chat section
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask a question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    response = requests.post(
        "http://localhost:8000/chat",
        json={"question": question}
    )

    answer = response.json()["answer"]

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)