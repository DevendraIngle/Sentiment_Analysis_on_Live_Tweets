import streamlit as st
import requests
import pandas as pd

st.title("Live Twitter Sentiment Analysis")
topic = st.text_input("Enter a topic to analyze:", "Python")

if st.button("Analyze"):
    with st.spinner("Fetching and analyzing tweets..."):
        response = requests.get("http://localhost:8000/sentiment", params={"topic": topic})
        if response.status_code == 200:
            data = response.json()["tweets"]
            df = pd.DataFrame(data)
            st.dataframe(df[["text", "label", "score"]])
            chart_data = df["label"].value_counts().rename_axis("label").reset_index(name="counts")
            st.write("### Sentiment Distribution")
            st.bar_chart(chart_data.set_index("label"))
        else:
            st.error("Failed to fetch sentiment data.")
