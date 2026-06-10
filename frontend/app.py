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
import pandas as pd

# ── Session state ──────────────────────────────────────────────────────────────
for key, default in [
    ("uploader_key", 0),
    ("messages", []),
]:
    if key not in st.session_state:
        st.session_state[key] = default


if "page" not in st.session_state:
    st.session_state.page = "chat"


def clear_quiz_state():
    st.session_state.quiz = None
    st.session_state.submitted = False
    st.session_state.score = 0
    st.session_state.quiz_meta = {
        "topic": "",
        "difficulty": "Easy",
    }

    for key in list(st.session_state.keys()):
        if key.startswith("question_"):
            del st.session_state[key]

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
            if st.session_state.page == "quiz":
                clear_quiz_state()
            st.session_state.page = "chat"

    with col2:
        if st.button("📊", key="nav_dashboard"):
            if st.session_state.page == "quiz":
                clear_quiz_state()
            st.session_state.page = "dashboard"

    with col3:
        if st.button("🔐", key="nav_login"):
            if st.session_state.page == "quiz":
                clear_quiz_state()
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

elif st.session_state.page == "dashboard":
    try:
        response = requests.get(
            "http://localhost:8000/dashboard",
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        st.error(f"Could not load dashboard data. Make sure the backend is running. Details: {e}")
        st.stop()

    st.markdown("## 📊 Dashboard")
    st.caption("Track quiz performance, topic strengths, weak areas, and recommendations.")

    total_quizzes = data.get("total_quizzes", 0)
    average_score = data.get("average_score", 0)
    topic_scores = data.get("topic_scores", [])
    difficulty_scores = data.get("difficulty_scores", [])
    quiz_history = data.get("quiz_history", [])
    strong_topics = data.get("strong_topics", [])
    weak_topics = data.get("weak_topics", [])
    recommendations = data.get("recommendations", [])

    if total_quizzes == 0:
        st.markdown("""
        <div class="hero">
            <div class="hero-ring">📊</div>
            <h2>No quiz data yet</h2>
            <p>Generate and submit a quiz to see your dashboard analytics.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Total Quizzes", total_quizzes)
    metric_2.metric("Average Score", f"{average_score}%")
    metric_3.metric("Strong Topics", len(strong_topics))
    metric_4.metric("Weak Topics", len(weak_topics))

    chart_left, chart_right = st.columns([1.25, 1])

    with chart_left:
        st.markdown("### Topic Performance")
        topic_df = pd.DataFrame(topic_scores)

        if not topic_df.empty:
            topic_df = topic_df.sort_values("score", ascending=False)
            st.bar_chart(topic_df, x="topic", y="score", use_container_width=True)
        else:
            st.info("No topic score data available yet.")

    with chart_right:
        st.markdown("### Difficulty Performance")
        difficulty_df = pd.DataFrame(difficulty_scores)

        if not difficulty_df.empty:
            difficulty_df = difficulty_df.sort_values("difficulty")
            st.bar_chart(difficulty_df, x="difficulty", y="score", use_container_width=True)
        else:
            st.info("No difficulty score data available yet.")

    insight_left, insight_mid, insight_right = st.columns(3)

    with insight_left:
        st.markdown("### Strong Topics")
        if strong_topics:
            for topic in strong_topics:
                st.success(topic)
        else:
            st.info("No strong topics yet.")

    with insight_mid:
        st.markdown("### Weak Topics")
        if weak_topics:
            for topic in weak_topics:
                st.error(topic)
        else:
            st.info("No weak topics yet.")

    with insight_right:
        st.markdown("### Recommendations")
        if recommendations:
            for recommendation in recommendations:
                st.warning(recommendation)
        else:
            st.info("Keep submitting quizzes to build recommendations.")

    st.markdown("### Quiz History")
    history_df = pd.DataFrame(quiz_history)

    if not history_df.empty:
        history_df = history_df.sort_values("id", ascending=False)
        history_df = history_df.rename(columns={
            "id": "ID",
            "topic": "Topic",
            "difficulty": "Difficulty",
            "score": "Score",
            "total": "Total",
            "percentage": "Percentage",
        })
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("No quiz history available yet.")

#quiz------------------------------------------------------------------
elif st.session_state.page == "quiz":
    with st.sidebar:
        st.markdown("### 📝 Quiz Settings")

        topic = st.text_input(
            "Topic",
            placeholder="Machine Learning",
            key="quiz_topic"
        )

        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            key="quiz_difficulty"
        )

        num_questions = st.slider(
            "Number of Questions",
            min_value=5,
            max_value=20,
            value=5,
            key="quiz_num_questions"
        )

        generate_quiz = st.button(
            "Generate Quiz",
            use_container_width=True
        )

        if st.session_state.get("quiz") is not None:
            reset_quiz = st.button(
                "New Quiz",
                use_container_width=True
            )

            if reset_quiz:
                clear_quiz_state()
                st.rerun()


    if "quiz" not in st.session_state:
        st.session_state.quiz = None

    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if "quiz_meta" not in st.session_state:
        st.session_state.quiz_meta = {
            "topic": "",
            "difficulty": "Easy",
        }

    if "score" not in st.session_state:
        st.session_state.score = 0

    if generate_quiz:

        topic = topic.strip()

        if not topic:
            st.sidebar.error("Please enter a topic first.")
            st.stop()

        try:
            uploaded_docs = requests.get(
                "http://localhost:8000/files",
                timeout=10,
            ).json()
        except requests.RequestException as e:
            st.error(f"Could not check uploaded PDFs. Make sure the backend is running. Details: {e}")
            st.stop()

        if not uploaded_docs:
            st.warning("Please upload a PDF before generating a quiz.")
            st.stop()

        for key in list(st.session_state.keys()):
            if key.startswith("question_"):
                del st.session_state[key]

        try:
            with st.spinner("Generating quiz..."):
                response = requests.post(
                    "http://localhost:8000/quiz",
                    json={
                        "topic": topic,
                        "difficulty": difficulty,
                        "num_questions": num_questions
                    },
                    timeout=60,
                )
                response.raise_for_status()
                quiz = response.json()
        except requests.HTTPError as e:
            try:
                detail = response.json().get("detail", str(e))
            except ValueError:
                detail = str(e)
            st.error(f"Could not generate quiz. {detail}")
            st.stop()
        except requests.RequestException as e:
            st.error(f"Could not generate quiz. Make sure the backend is running. Details: {e}")
            st.stop()
        except ValueError:
            st.error("The backend returned an invalid quiz response.")
            st.stop()

        if not isinstance(quiz, list) or not quiz:
            st.error("No quiz questions were returned for this topic.")
            st.stop()

        st.session_state.quiz = quiz
        st.session_state.quiz_meta = {
            "topic": topic,
            "difficulty": difficulty,
        }
        st.session_state.submitted = False
        st.session_state.score = 0
        st.rerun()


    if st.session_state.quiz is None:
        st.markdown("""
        <div class="hero">
            <div class="hero-ring">📝</div>
            <h2>Generate a Quiz</h2>
            <p>Select a topic and difficulty from the sidebar. StudyMate will create a practice quiz from your study material.</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("## 📝 Quiz")
        st.caption(
            f"Topic: {st.session_state.quiz_meta['topic']} | "
            f"Difficulty: {st.session_state.quiz_meta['difficulty']}"
        )

        with st.form("quiz_answer_form"):
            user_answers = {}

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

                user_answers[i] = st.radio(
                    "",
                    q["options"],
                    key=f"question_{i}",
                    index=None,
                    label_visibility="collapsed",
                )

            submit_quiz = st.form_submit_button(
                "Submit Quiz",
                use_container_width=True
            )

        if submit_quiz:

            unanswered = []

            for i in range(1, len(st.session_state.quiz) + 1):
                if st.session_state.get(f"question_{i}") is None:
                    unanswered.append(i)

            if unanswered:
                st.error(
                    f"Please answer all questions. Missing: {', '.join(map(str, unanswered))}"
                )
                st.stop()

            score = 0

            for i, q in enumerate(st.session_state.quiz, start=1):

                if user_answers.get(i) == q["answer"]:
                    score += 1

            try:
                response = requests.post(
                    "http://localhost:8000/submit-quiz",
                    json={
                        "topic": st.session_state.quiz_meta["topic"],
                        "difficulty": st.session_state.quiz_meta["difficulty"],
                        "score": score,
                        "total": len(st.session_state.quiz),
                    },
                    timeout=15,
                )
                response.raise_for_status()
                st.session_state.score = score
                st.session_state.submitted = True
            except requests.RequestException as e:
                st.error(f"Failed to save quiz result: {e}")


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
