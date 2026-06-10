# import streamlit as st
# import requests

# topic = st.text_input("Topic")

# difficulty = st.selectbox(
#     "Difficulty",["Easy","Medium","Hard"]
# )

# if st.button("Generate Quiz"):
#     response = requests.post(
#         "http://localhost:8000/quiz",
#         json={
#             "topic": topic,
#             "difficulty": difficulty,
#             "num_questions": 5
#         }
#     )

#     quiz = response.json()

#     st.json(quiz)
import streamlit as st
import requests

st.set_page_config(
    page_title="StudyMate Quiz",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

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
    border-radius:14px;
    padding:24px;
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
        placeholder="Machine Learning"
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy","Medium","Hard"]
    )

    generate_quiz = st.button(
        "Generate Quiz",
        use_container_width=True
    )

# GENERATE QUIZ
if generate_quiz:

    st.session_state.submitted = False

    try:

        response = requests.post(
            "http://localhost:8000/quiz",
            json={
                "topic": topic,
                "difficulty": difficulty,
                "num_questions": 5
            }
        )

        st.session_state.quiz = response.json()

    except Exception as e:
        st.error(f"Error: {e}")

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

    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)

    st.title("📝 Quiz")

    user_answers = {}

    for i, q in enumerate(quiz, start=1):

        st.markdown(f"### Q{i}. {q['question']}")

        user_answers[i] = st.radio(
            "",
            q["options"],
            key=f"question_{i}"
        )

        st.divider()

    if st.button("Submit Quiz"):

        score = 0

        for i, q in enumerate(quiz, start=1):

            if user_answers[i] == q["answer"]:
                score += 1

        st.session_state.submitted = True
        st.session_state.score = score

    if st.session_state.submitted:

        st.success(
            f"Your Score: {st.session_state.score}/{len(quiz)}"
        )

        st.subheader("Correct Answers")

        for i, q in enumerate(quiz, start=1):

            st.write(
                f"Q{i}: {q['answer']}"
            )

    st.markdown('</div>', unsafe_allow_html=True)