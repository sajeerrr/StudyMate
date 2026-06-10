import streamlit as st
import requests

import pandas as pd
import matplotlib.pyplot as plt

data = requests.get(
    "http://localhost:8000/dashboard",
).json()

st.metric(
    "Average Score",
    data["average_score"]
)

st.write(
    "Strong Topics",
    data["strong_topics"]
)

st.write(
    "Weak Topics",
    data["weak_topics"]
)



#chart
df = pd.DataFrame(
    data["topic_scores"]
)

fig, ax = plt.subplots()

ax.bar(
    df["topic"],
    df["score"]
)

st.pyplot(fig)