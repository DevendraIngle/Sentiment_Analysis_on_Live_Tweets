import tweepy
import os
import time
from dotenv import load_dotenv
from utils import clean_tweet

load_dotenv()  

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
if not BEARER_TOKEN:
    raise ValueError("TWITTER_BEARER_TOKEN not found in environment variables")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_tweets(keyword, max_results=10, max_retries=3):
    retry_count = 0
    base_delay = 1  
    
    while retry_count < max_retries:
        try:
            query = f"{keyword} -is:retweet lang:en"
            response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["text"])
            
            if not response.data:
                return []
                
            raw_tweets = [tweet.text for tweet in response.data]
            tweets = [clean_tweet(t) for t in raw_tweets]
            return tweets
            
        except tweepy.TooManyRequests as e:
            retry_count += 1
            if retry_count == max_retries:
                print(f"Max retries reached. Rate limit error: {str(e)}")
                return []
                
            
            delay = base_delay * (2 ** (retry_count - 1))
            print(f"Rate limit hit. Waiting {delay} seconds before retry {retry_count}/{max_retries}")
            time.sleep(delay)
            
        except tweepy.TweepyException as e:
            print(f"Error fetching tweets: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return []
