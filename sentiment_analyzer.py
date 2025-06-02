from transformers import pipeline
from collections import Counter
from models import TweetSentiment, SentimentResponse

classifier = pipeline("sentiment-analysis")

def analyze_sentiments(tweets: list):
    results = classifier(tweets)
    sentiments = [res["label"] for res in results]

    counts = Counter(sentiments)
    summary = {
        "positive": counts.get("POSITIVE", 0),
        "negative": counts.get("NEGATIVE", 0),
        "neutral": counts.get("NEUTRAL", 0)  
    }

    tagged = []
    for tweet, res in zip(tweets, results):
        tagged.append(TweetSentiment(text=tweet, label=res["label"], score=round(res["score"], 4)))

    return SentimentResponse(summary=summary, tweets=tagged)