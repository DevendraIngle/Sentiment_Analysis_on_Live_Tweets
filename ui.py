import streamlit as st
import requests
import pandas as pd
from requests.exceptions import RequestException
import os
import plotly.express as px


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Twitter Sentiment Analysis")

st.title("Live Twitter Sentiment Analysis")
st.markdown("Analyze the sentiment of recent tweets about any topic!")


with st.sidebar:
    st.header("Sample Topics")
    sample_topics = ["Python", "AI", "Machine Learning", "Data Science", "Programming"]
    for topic in sample_topics:
        if st.button(topic, key=topic):
            st.session_state.topic = topic


topic = st.text_input("Enter a topic to analyze:", 
                     value=st.session_state.get('topic', 'Python'))

if st.button("Analyze"):
    try:
        with st.spinner("Fetching and analyzing tweets..."):
            response = requests.get(f"{API_URL}/sentiment", 
                                 params={"topic": topic},
                                 timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                
                st.subheader("Sentiment Summary")
                summary = data.get("summary", {})
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Positive", summary.get("positive", 0))
                with col2:
                    st.metric("Negative", summary.get("negative", 0))
                with col3:
                    st.metric("Neutral", summary.get("neutral", 0))
                
                
                st.subheader("Analyzed Tweets")
                tweets_data = data.get("tweets", [])
                if tweets_data:
                    df = pd.DataFrame(tweets_data)
                    st.dataframe(df[["text", "label", "score"]])
                    
                    
                    st.subheader("Sentiment Distribution")
                    chart_data = df["label"].value_counts().rename_axis("label").reset_index(name="counts")
                    
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("Bar Chart")
                        st.bar_chart(chart_data.set_index("label"))
                    
                    with col2:
                        st.write("Pie Chart")
                        fig = px.pie(chart_data, 
                                   values='counts', 
                                   names='label',
                                   title='Sentiment Distribution',
                                   color_discrete_sequence=px.colors.qualitative.Set3)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No tweets found for this topic.")
                    
            elif response.status_code == 404:
                st.warning("No tweets found for this topic. Try a different search term.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
    except RequestException as e:
        st.error("Failed to connect to the server. Please make sure the API is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
