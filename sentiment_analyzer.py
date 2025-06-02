from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from collections import Counter
from models import TweetSentiment, SentimentResponse


_classifier = None

def get_classifier():
    """Lazy load the sentiment classifier"""
    global _classifier
    if _classifier is None:
        try:
            """
            Currently, the model in use is distilbert-base-uncased-finetuned-sst-2-english, a lightweight and efficient transformer fine-tuned for sentiment analysis. While it offers a good balance between speed and accuracy, for improved performance and more nuanced emotion detection, consider using larger and more advanced models such as:

            cardiffnlp/twitter-roberta-base-emotion-multilabel-latest – ideal for multi-label emotion classification, especially on social media data.

            Other larger models like bert-base-uncased, roberta-base, or xlm-roberta-large can also provide higher accuracy at the cost of increased computational resources.
            
            """
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            _classifier = pipeline(
                "sentiment-analysis",
                model=model_name,
                device=-1  
            )
        except Exception as e:
            raise Exception(f"Error loading sentiment classifier: {str(e)}")
    return _classifier

def analyze_sentiments(tweets: list):

    if not tweets:
        raise ValueError("No tweets provided for analysis")
        
    try:
        classifier = get_classifier()
        results = classifier(tweets)
        
       
        sentiments = [res["label"] for res in results]
        counts = Counter(sentiments)
        
        
        summary = {
            "positive": counts.get("POSITIVE", 0),
            "negative": counts.get("NEGATIVE", 0),
            "neutral": 0  
        }
        
        
        tagged = []
        for tweet, res in zip(tweets, results):
            tagged.append(TweetSentiment(
                text=tweet,
                label=res["label"],
                score=round(res["score"], 4)
            ))
            
            
        return SentimentResponse(summary=summary, tweets=tagged)
        
    except Exception as e:
        raise Exception(f"Error in sentiment analysis: {str(e)}")