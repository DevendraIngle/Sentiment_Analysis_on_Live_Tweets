from fastapi import FastAPI, Query
from sentiment_analyzer import analyze_sentiment
from twitter_fetcher import fetch_tweets
from models import SentimentResponse

app = FastAPI()


@app.get("/sentiment", response_model=SentimentResponse)
def get_sentiment(topic: str = Query(..., description="Topic to search tweets for")):
    tweets = fetch_tweets(topic)
    sentiments = [analyze_sentiment(tweet) for tweet in tweets]
    return SentimentResponse(tweets=sentiments)
