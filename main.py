from fastapi import FastAPI, Query, HTTPException
from sentiment_analyzer import analyze_sentiments
from twitter_fetcher import fetch_tweets
from models import SentimentResponse

app = FastAPI()


@app.get("/sentiment", response_model=SentimentResponse)
async def get_sentiment(topic: str = Query(..., description="Topic to search tweets for")):
    try:
        # Fetch tweets for the topic
        tweets = fetch_tweets(topic)
        if not tweets:
            raise HTTPException(status_code=404, detail="No tweets found for the given topic")
            
        # Analyze sentiments for all tweets at once
        sentiment_result = analyze_sentiments(tweets)
        return sentiment_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
