import pandas as pd
import requests
import streamlit as st


API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="StudyMate Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp {
    background: #0d1117;
    color: #e6edf3;
}

[data-testid="stSidebar"] {
    background: #161b27 !important;
    border-right: 1px solid #21293d;
}

.dashboard-hero {
    border-bottom: 1px solid #21293d;
    padding: 8px 0 18px;
    margin-bottom: 18px;
}

.dashboard-hero h1 {
    color: #f1f5f9;
    font-size: 30px;
    margin: 0 0 6px;
}

.dashboard-hero p {
    color: #8b949e;
    margin: 0;
}

.section-title {
    color: #f1f5f9;
    font-size: 18px;
    font-weight: 700;
    margin: 18px 0 8px;
}

.empty-state {
    min-height: 55vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: #8b949e;
}

.empty-state h2 {
    color: #f1f5f9;
    font-size: 24px;
    margin-bottom: 8px;
}

[data-testid="stMetric"] {
    background: #161b27;
    border: 1px solid #21293d;
    border-radius: 8px;
    padding: 14px 16px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #21293d;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


def fetch_dashboard():
    response = requests.get(
        f"{API_URL}/dashboard",
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


try:
    data = fetch_dashboard()
except requests.RequestException as e:
    st.error(f"Could not load dashboard data. Make sure the backend is running. Details: {e}")
    st.stop()


st.markdown("""
<div class="dashboard-hero">
    <h1>StudyMate Dashboard</h1>
    <p>Track quiz performance, topic strengths, weak areas, and practice recommendations.</p>
</div>
""", unsafe_allow_html=True)

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
    <div class="empty-state">
        <div>
            <h2>No quiz data yet</h2>
            <p>Generate and submit a quiz to see your analytics here.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

score_label = f"{average_score:.2f}%" if isinstance(average_score, float) else f"{average_score}%"

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Total Quizzes", total_quizzes)
metric_2.metric("Average Score", score_label)
metric_3.metric("Strong Topics", len(strong_topics))
metric_4.metric("Weak Topics", len(weak_topics))

left, right = st.columns([1.25, 1])

with left:
    st.markdown('<div class="section-title">Topic Performance</div>', unsafe_allow_html=True)
    topic_df = pd.DataFrame(topic_scores)

    if not topic_df.empty:
        topic_df = topic_df.sort_values("score", ascending=False)
        st.bar_chart(
            topic_df,
            x="topic",
            y="score",
            use_container_width=True,
        )
    else:
        st.info("No topic score data available yet.")

with right:
    st.markdown('<div class="section-title">Difficulty Performance</div>', unsafe_allow_html=True)
    difficulty_df = pd.DataFrame(difficulty_scores)

    if not difficulty_df.empty:
        difficulty_df = difficulty_df.sort_values("difficulty")
        st.bar_chart(
            difficulty_df,
            x="difficulty",
            y="score",
            use_container_width=True,
        )
    else:
        st.info("No difficulty score data available yet.")

st.markdown('<div class="section-title">Topic Insights</div>', unsafe_allow_html=True)
insight_left, insight_mid, insight_right = st.columns(3)

with insight_left:
    st.subheader("Strong Topics")
    if strong_topics:
        for topic in strong_topics:
            st.success(topic)
    else:
        st.info("No strong topics yet.")

with insight_mid:
    st.subheader("Weak Topics")
    if weak_topics:
        for topic in weak_topics:
            st.error(topic)
    else:
        st.info("No weak topics yet.")

with insight_right:
    st.subheader("Recommendations")
    if recommendations:
        for recommendation in recommendations:
            st.warning(recommendation)
    else:
        st.info("Keep submitting quizzes to build recommendations.")

st.markdown('<div class="section-title">Quiz History</div>', unsafe_allow_html=True)
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
    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No quiz history available yet.")
