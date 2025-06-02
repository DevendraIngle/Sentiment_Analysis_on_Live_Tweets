import tweepy
import os
from dotenv import load_dotenv
from utils import clean_tweet

load_dotenv()  

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_tweets(keyword, max_results=20):
    query = f"{keyword} -is:retweet lang:en"
    response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["text"])
    raw_tweets = [tweet.text for tweet in response.data] if response.data else []

    tweets = [clean_tweet(t) for t in raw_tweets]
    return tweets
