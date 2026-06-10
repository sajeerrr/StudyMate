import streamlit as st
import requests

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "center_key" not in st.session_state:
    st.session_state.center_key = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

if "upload_success" not in st.session_state:
    st.session_state.upload_success = False

st.set_page_config(
    page_title="StudyMate",
    layout="wide"
)

#------------------------------------------------------------------
#sidebar name hide
#------------------------------------------------------------------
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.title("StudyMate")

#left-top alignment style
st.markdown("""
<style>
.docs-container {
    max-height: 350px;
    overflow-y: auto;
    padding-right: 5px;
}

.big-upload {
    border: 2px dashed #666;
    border-radius: 15px;
    padding: 40px;
    text-align: center;
    margin-top: 50px;
    margin-bottom: 50px;
}
</style>
""", unsafe_allow_html=True)

#---------------------------------------------------------------------
#sidebar-upload
#---------------------------------------------------------------------

with st.sidebar:

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.page_link(
            "app.py",
            label="",
            icon="💬"
        )

    with c2:
        st.page_link(
            "pages/dashboard.py",
            label="",
            icon="📊"
        )

    with c3:
        st.page_link(
            "pages/login.py",
            label="",
            icon="🔐"
        )

    with c4:
        st.page_link(
            "pages/quiz.py",
            label="",
            icon="📝"
        )

st.sidebar.markdown("---")
st.sidebar.title("Documents")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"],
    key=f"uploader_{st.session_state.uploader_key}"
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
        st.session_state.uploader_key += 1
        st.rerun()
#------------------------------------------------------------------------
#large upload
#------------------------------------------------------------------------

docs=[]

try:
    docs = requests.get(
        "http://localhost:8000/files"
    ).json()
except Exception as e:
    st.sidebar.error(str(e))

show_upload_card = (
    len(st.session_state.messages) == 0
    and len(docs) == 0
)


if show_upload_card:

    st.markdown(
        """
        <div class="big-upload">
            <h1>📄 Upload Documents</h1>
            <p>Upload PDFs and start chatting with them.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    center_upload = st.file_uploader(
        "",
        type=["pdf"],
        label_visibility="collapsed",
        key=f"center_upload_{st.session_state.center_key}"
    )

    if center_upload:

        if st.button("Upload Document"):

            files = {
                "file": (
                    center_upload.name,
                    center_upload,
                    "application/pdf"
                )
            }

            with st.spinner(
                "Processing PDF..."
            ):

                response = requests.post(
                    "http://localhost:8000/upload",
                    files=files
                )

            st.session_state.center_key += 1
            st.session_state.upload_success = True

            st.rerun()
#------------------------------------------------------------------
#Document list in sidebar
#-------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Uploaded Documents")

st.sidebar.markdown('<div class="docs-container">', unsafe_allow_html=True)

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

st.sidebar.markdown("</div>", unsafe_allow_html=True)

#------------------------------------------------------------------
#chat section
#------------------------------------------------------------------
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

