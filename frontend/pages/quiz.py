import streamlit as st
import requests
from html import escape

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="StudyMate Quiz",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

st.markdown("""
<style>

.stApp{
    background:#0d1117;
    color:#e6edf3;
}

[data-testid="stSidebar"]{
    background:#161b27 !important;
    border-right:1px solid #21293d;
}

.sb-header{
    display:flex;
    align-items:center;
    gap:10px;
    padding:18px 16px;
    border-bottom:1px solid #21293d;
}

.sb-logo{
    width:34px;
    height:34px;
    border-radius:9px;
    background:linear-gradient(135deg,#2563eb,#6366f1);
    display:flex;
    align-items:center;
    justify-content:center;
}

.sb-brand{
    color:#f1f5f9;
    font-weight:700;
}

.sb-sub{
    color:#6b7280;
    font-size:11px;
}

.hero{
    min-height:70vh;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
}

.hero-ring{
    width:80px;
    height:80px;
    border-radius:20px;
    background:#161b27;
    border:1px solid #21293d;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:36px;
    margin-bottom:20px;
}

.hero h2{
    color:#f1f5f9;
}

.hero p{
    color:#8b949e;
}

.quiz-card{
    background:#161b27;
    border:1px solid #21293d;
    border-radius:8px;
    padding:24px;
    margin-top:18px;
}

.quiz-meta{
    color:#8b949e;
    font-size:14px;
    margin-bottom:16px;
}

.answer-row{
    border:1px solid #21293d;
    border-radius:8px;
    padding:12px 14px;
    margin-bottom:10px;
    background:#0d1117;
}

.stButton button{
    width:100%;
    background:linear-gradient(135deg,#2563eb,#5b56e8) !important;
    color:white !important;
    border:none !important;
    border-radius:8px !important;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:

    st.markdown("""
    <div class="sb-header">
        <div class="sb-logo">📝</div>
        <div>
            <div class="sb-brand">StudyMate</div>
            <div class="sb-sub">Quiz Generator</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Quiz Settings")

    topic = st.text_input(
        "Topic",
        placeholder="Machine Learning",
        value=st.session_state.quiz_meta.get("topic", "")
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"],
        index=["Easy", "Medium", "Hard"].index(
            st.session_state.quiz_meta.get("difficulty", "Easy")
        )
    )

    num_questions = st.slider(
        "Questions",
        min_value=5,
        max_value=20,
        value=5
    )

    generate_quiz = st.button(
        "Generate Quiz",
        use_container_width=True
    )

    if st.session_state.quiz is not None:
        reset_quiz = st.button(
            "New Quiz",
            use_container_width=True
        )

        if reset_quiz:
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

            st.rerun()

# GENERATE QUIZ
if generate_quiz:

    topic = topic.strip()

    if not topic:
        st.sidebar.error("Please enter a topic first.")
        st.stop()

    try:
        uploaded_docs = requests.get(
            f"{API_URL}/files",
            timeout=10,
        ).json()
    except requests.RequestException as e:
        st.error(f"Could not check uploaded PDFs. Make sure the backend is running. Details: {e}")
        st.stop()

    if not uploaded_docs:
        st.warning("Please upload a PDF before generating a quiz.")
        st.stop()

    st.session_state.submitted = False
    st.session_state.score = 0
    st.session_state.quiz_meta = {
        "topic": topic,
        "difficulty": difficulty,
    }

    # Clear old answers
    for key in list(st.session_state.keys()):
        if key.startswith("question_"):
            del st.session_state[key]

    try:
        with st.spinner("Generating quiz..."):
            response = requests.post(
                f"{API_URL}/quiz",
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

    st.rerun()

# HERO SCREEN
if st.session_state.quiz is None:

    st.markdown("""
    <div class="hero">
        <div class="hero-ring">📝</div>

        <h2>Generate a Quiz</h2>

        <p>
        Select a topic and difficulty from the sidebar.
        StudyMate will instantly create a quiz for practice.
        </p>

    </div>
    """, unsafe_allow_html=True)

# QUIZ SCREEN
else:

    quiz = st.session_state.quiz
    saved_topic = st.session_state.quiz_meta.get("topic", topic)
    saved_difficulty = st.session_state.quiz_meta.get("difficulty", difficulty)
    topic_label = escape(saved_topic)
    difficulty_label = escape(saved_difficulty)

    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)

    st.title("Quiz")
    st.markdown(
        f'<div class="quiz-meta">Topic: {topic_label} | Difficulty: {difficulty_label}</div>',
        unsafe_allow_html=True,
    )

    with st.form("quiz_answer_form"):
        user_answers = {}

        for i, q in enumerate(quiz, start=1):

            question = q.get("question", f"Question {i}")
            options = q.get("options", [])

            st.markdown(f"### Q{i}. {question}")

            if not options:
                st.warning("This question has no answer options.")
                continue

            user_answers[i] = st.radio(
                label="",
                options=options,
                key=f"question_{i}",
                index=None,
                label_visibility="collapsed"
            )
            st.divider()

        submit_quiz = st.form_submit_button(
            "Submit Quiz",
            use_container_width=True
        )

    if submit_quiz:

        unanswered = []

        for i in range(1, len(quiz) + 1):
            if st.session_state.get(f"question_{i}") is None:
                unanswered.append(i)

        if unanswered:
            st.error(
                f"Please answer all questions. Missing: {', '.join(map(str, unanswered))}"
            )
            st.stop()

        score = 0

        for i, q in enumerate(quiz, start=1):
            if user_answers.get(i) == q.get("answer"):
                score += 1

        try:
            response = requests.post(
                f"{API_URL}/submit-quiz",
                json={
                    "topic": saved_topic,
                    "difficulty": saved_difficulty,
                    "score": score,
                    "total": len(quiz)
                },
                timeout=15,
            )
            response.raise_for_status()
            st.session_state.submitted = True
            st.session_state.score = score

        except Exception as e:
            st.error(f"Failed to save result: {e}")

    if st.session_state.submitted:

        st.success(
            f"Your Score: {st.session_state.score}/{len(quiz)}"
        )

        st.subheader("Correct Answers")

        for i, q in enumerate(quiz, start=1):
            selected = st.session_state.get(f"question_{i}")
            answer = q.get("answer", "")

            if selected == answer:
                st.success(f"Q{i}: {answer}")
            else:
                st.error(f"Q{i}: Your answer: {selected} | Correct answer: {answer}")

    st.markdown('</div>', unsafe_allow_html=True)
