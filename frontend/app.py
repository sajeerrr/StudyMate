# import streamlit as st
# import requests

# if "uploader_key" not in st.session_state:
#     st.session_state.uploader_key = 0

# if "center_key" not in st.session_state:
#     st.session_state.center_key = 0

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "upload_success" not in st.session_state:
#     st.session_state.upload_success = False

# st.set_page_config(
#     page_title="StudyMate",
#     layout="wide"
# )

# #------------------------------------------------------------------
# #sidebar name hide
# #------------------------------------------------------------------
# st.markdown("""
# <style>
# [data-testid="stSidebarNav"] {
#     display: none;
# }
# </style>
# """, unsafe_allow_html=True)

# st.title("StudyMate")

# #-------------------------------------------------------
# #left-top alignment style
# #-------------------------------------------------------

# st.markdown("""
# <style>
# .docs-container {
#     max-height: 350px;
#     overflow-y: auto;
#     padding-right: 5px;
# }

# .big-upload {
#     border: 2px dashed #666;
#     border-radius: 15px;
#     padding: 40px;
#     text-align: center;
#     margin-top: 50px;
#     margin-bottom: 50px;
# }
# </style>
# """, unsafe_allow_html=True)

# #---------------------------------------------------------------------
# #sidebar-upload
# #---------------------------------------------------------------------

# with st.sidebar:

#     c1, c2, c3, c4 = st.columns(4)

#     with c1:
#         st.page_link("app.py",label="",icon="💬")

#     with c2:
#         st.page_link("pages/dashboard.py",label="",icon="📊")

#     with c3:
#         st.page_link("pages/login.py",label="",icon="🔐")

#     with c4:
#         st.page_link("pages/quiz.py",label="",icon="📝")

# #-----------------------------------------------------------
# #documents-upload
# #-----------------------------------------------------------

# st.sidebar.markdown("---")
# st.sidebar.title("Documents")

# uploaded_file = st.sidebar.file_uploader(
#     "Upload PDF",
#     type=["pdf"],
#     key=f"uploader_{st.session_state.uploader_key}"
# )

# if uploaded_file:

#     if st.sidebar.button("Upload"):
#         files = {
#             "file":(
#                 uploaded_file.name,
#                 uploaded_file,
#                 "application/pdf"
#             )
#         }

#         with st.sidebar:
#             with st.spinner("Processing PDF..."):
#                 response = requests.post(
#                     "http://localhost:8000/upload",
#                     files=files
#                 )

#         st.sidebar.success(
#             response.json()["message"]
#         )
#         st.session_state["upload_success"] = True
#         st.session_state.uploader_key += 1
#         st.rerun()


# docs=[]

# try:
#     docs = requests.get(
#         "http://localhost:8000/files"
#     ).json()
# except Exception as e:
#     st.sidebar.error(str(e))

# #------------------------------------------------------------
# #large upload
# #------------------------------------------------------------

# if len(st.session_state.messages) == 0:

#     st.markdown(
#         """
#         <div class="big-upload">
#             <h1>📄 Upload Documents</h1>
#             <p>Upload PDFs and start chatting with them.</p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     center_upload = st.file_uploader(
#         "",
#         type=["pdf"],
#         label_visibility="collapsed",
#         key=f"center_upload_{st.session_state.center_key}"
#     )

#     if center_upload and st.button("Upload Document"):

#         files = {
#             "file": (
#                 center_upload.name,
#                 center_upload,
#                 "application/pdf"
#             )
#         }

#         with st.spinner(
#             "Processing PDF..."
#         ):
#             response = requests.post(
#                 "http://localhost:8000/upload",
#                 files=files
#             )

#         st.session_state.center_key += 1
#         st.session_state.upload_success = True

#         st.rerun()

# #------------------------------------------------------------------
# #Document list in sidebar
# #-------------------------------------------------------------------
# st.sidebar.markdown("---")
# st.sidebar.subheader("Uploaded Documents")

# st.sidebar.markdown('<div class="docs-container">', unsafe_allow_html=True)

# for doc in docs:
#     col1, col2 = st.sidebar.columns([4, 1])

#     with col1:
#         st.write(doc["name"])
#     with col2:
#         if st.button("🗑️",key=doc["file_id"]):
#             requests.delete(
#                 f"http://localhost:8000/pdf/{doc['file_id']}"
#             )
#             st.rerun()

# st.sidebar.markdown("</div>", unsafe_allow_html=True)

# #------------------------------------------------------------------
# #chat section
# #------------------------------------------------------------------
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])

# question = st.chat_input("Ask a question...")

# if question:
#     st.session_state.messages.append({
#         "role": "user",
#         "content": question
#     })

#     with st.chat_message("user"):
#         st.write(question)

#     response = requests.post(
#         "http://localhost:8000/chat",
#         json={"question": question}
#     )

#     answer = response.json()["answer"]

#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": answer
#     })

#     with st.chat_message("assistant"):
#         st.write(answer)


import streamlit as st
import requests

# ── Session state ──────────────────────────────────────────────────────────────
for key, default in [
    ("uploader_key", 0),
    ("messages", []),
]:
    if key not in st.session_state:
        st.session_state[key] = default


if "page" not in st.session_state:
    st.session_state.page = "chat"

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StudyMate",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global styles ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebarNav"] { display: none; }

.stApp { background-color: #0d1117; color: #e6edf3; }

[data-testid="stSidebar"] {
    background-color: #161b27 !important;
    border-right: 1px solid #21293d;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}
section[data-testid="stSidebar"] > div {
    padding: 0 !important;
    gap: 0 !important;
}

.sb-header {
    display: flex; align-items: center; gap: 10px;
    padding: 18px 16px 14px;
    border-bottom: 1px solid #21293d;
}
.sb-logo {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #2563eb, #6366f1);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px; flex-shrink: 0;
}
.sb-brand { font-size: 30px; font-weight: 700; color: #f1f5f9; letter-spacing: -0.02em; }
.sb-sub   { font-size: 11px; color: #4a566a; margin-top: 1px; }

.sb-nav {
    display: flex; gap: 5px;
    padding: 10px 12px;
    border-bottom: 1px solid #21293d;
}
.sb-nav a {
    flex: 1; height: 34px;
    background: #1c2333; border: 1px solid #21293d; border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; text-decoration: none; color: #8b949e;
    transition: background .15s;
}
.sb-nav a:hover { background: #222d42; color: #e6edf3; }

.sb-label {
    font-size: 10px; font-weight: 600;
    letter-spacing: 0.09em; text-transform: uppercase;
    color: #4a566a; padding: 12px 16px 6px;
}

.sb-divider { height: 1px; background: #21293d; margin: 4px 0; }

.doc-card {
    display: flex; align-items: center; gap: 9px;
    padding: 8px 10px;
    background: #1c2333; border: 1px solid #21293d; border-radius: 8px;
    margin: 0 12px 5px;
}
.doc-icon {
    width: 26px; height: 26px;
    background: linear-gradient(135deg, #1a3a6e, #2563eb);
    border-radius: 6px; display: flex; align-items: center;
    justify-content: center; font-size: 12px; flex-shrink: 0;
}
.doc-name {
    flex: 1; font-size: 12px; color: #cbd5e1;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.docs-empty {
    text-align: center; padding: 20px 16px;
    color: #2d3748; font-size: 12px; line-height: 1.8;
}

[data-testid="stFileUploaderDropzone"] {
    background: #1c2333 !important;
    border: 1.5px dashed #2d3f5e !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploaderDropzone"] p { color: #4a566a !important; font-size: 12px !important; }

.hero {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; min-height: 62vh;
}
.hero-ring {
    width: 76px; height: 76px;
    background: #161b27; border: 1px solid #21293d; border-radius: 20px;
    display: flex; align-items: center; justify-content: center;
    font-size: 34px; margin-bottom: 22px;
    box-shadow: 0 0 36px rgba(47,129,247,0.07);
}
.hero h2 {
    font-size: 22px; font-weight: 700; color: #f1f5f9;
    letter-spacing: -0.03em; margin-bottom: 10px;
}
.hero p { font-size: 14px; color: #8b949e; max-width: 360px; line-height: 1.7; margin: 0 auto; }



[data-testid="stChatInput"] {
    background: #161b27 !important; border: 1.5px solid #21293d !important;
    border-radius: 12px !important; color: #e6edf3 !important;
}


.stSuccess { background: #0d2b17 !important; border-color: #1a4d2e !important; color: #4ade80 !important; border-radius: 8px !important; }
.stError   { background: #2d0f0f !important; border-radius: 8px !important; }
.main .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #21293d; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-header">
        <div class="sb-logo">📚</div>
        <div>
            <div class="sb-brand">StudyMate</div>
            <div class="sb-sub">PDF Chat Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='height:15px'></div>",
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💬", key="nav_chat"):
            st.session_state.page = "chat"

    with col2:
        if st.button("📊", key="nav_dashboard"):
            st.session_state.page = "dashboard"

    with col3:
        if st.button("🔐", key="nav_login"):
            st.session_state.page = "login"

    with col4:
        if st.button("📝", key="nav_quiz"):
            st.session_state.page = "quiz"


    st.markdown('<div class="sb-label">Upload Document</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["pdf"],
        key=f"uploader_{st.session_state.uploader_key}",
        label_visibility="collapsed",
    )

    if uploaded_file:
        if st.button("Upload PDF", use_container_width=True):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            with st.spinner("Processing…"):
                try:
                    response = requests.post("http://localhost:8000/upload", files=files)
                    st.success(response.json().get("message", "Uploaded!"))
                except Exception as e:
                    st.error(f"Upload failed: {e}")
            st.session_state.uploader_key += 1
            st.rerun()

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-label">Documents</div>', unsafe_allow_html=True)

    docs = []
    try:
        docs = requests.get("http://localhost:8000/files").json()
    except Exception:
        pass

    if docs:
        for doc in docs:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div class="doc-card">
                    <div class="doc-icon">📄</div>
                    <div class="doc-name" title="{doc['name']}">{doc['name']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✕", key=doc["file_id"], help="Remove"):
                    try:
                        requests.delete(f"http://localhost:8000/pdf/{doc['file_id']}")
                    except Exception:
                        pass
                    st.rerun()
    else:
        st.markdown("""
        <div class="docs-empty">No documents yet.<br>Upload a PDF to begin.</div>
        """, unsafe_allow_html=True)


# ── Main ───────────────────────────────────────────────────────────────────────
if st.session_state.page == "chat":
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="hero">
            <div class="hero-ring">📖</div>
            <h2>What do you want to learn?</h2>
            <p>Upload a PDF and start asking questions. StudyMate will find answers directly from your documents.</p>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask a question about your documents…")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Thinking…"):
            try:
                response = requests.post("http://localhost:8000/chat", json={"question": question})
                answer = response.json()["answer"]
            except Exception as e:
                answer = f"⚠️ Could not reach the server: {e}"

        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.write(answer)

#quiz------------------------------------------------------------------
elif st.session_state.page == "quiz":
    with st.sidebar:
        st.markdown("### 📝 Quiz Settings")

        topic = st.text_input(
            "Topic",
            placeholder="Machine Learning"
        )

        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"]
        )

        num_questions = st.slider(
            "Number of Questions",
            min_value=5,
            max_value=20,
            value=5
        )

        generate_quiz = st.button(
            "Generate Quiz",
            use_container_width=True
        )


    if "quiz" not in st.session_state:
        st.session_state.quiz = None

    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if generate_quiz:

        response = requests.post(
            "http://localhost:8000/quiz",
            json={
                "topic": topic,
                "difficulty": difficulty,
                "num_questions": num_questions
            }
        )

        st.session_state.quiz = response.json()
        st.session_state.submitted = False


    if st.session_state.quiz:

        st.markdown("## 📝 Quiz")

        score = 0

        for i, q in enumerate(st.session_state.quiz, start=1):

            st.markdown(f"""
            <div style="
                background:#161b27;
                border:1px solid #21293d;
                border-radius:12px;
                padding:18px;
                margin-bottom:15px;
            ">
            <h4>Q{i}. {q['question']}</h4>
            </div>
            """, unsafe_allow_html=True)

            st.radio(
                "",
                q["options"],
                key=f"question_{i}"
            )

        if st.button("Submit Quiz", use_container_width=True):

            for i, q in enumerate(st.session_state.quiz, start=1):

                if st.session_state[f"question_{i}"] == q["answer"]:
                    score += 1

            st.session_state.score = score
            st.session_state.submitted = True


    if st.session_state.submitted:

        st.success(
            f"Score: {st.session_state.score}/{len(st.session_state.quiz)}"
        )

        st.markdown("### Correct Answers")

        for i, q in enumerate(st.session_state.quiz, start=1):

            selected = st.session_state[f"question_{i}"]

            if selected == q["answer"]:
                st.success(f"Q{i}: {q['answer']}")
            else:
                st.error(
                    f"Q{i}: Your Answer = {selected} | Correct = {q['answer']}"
                )