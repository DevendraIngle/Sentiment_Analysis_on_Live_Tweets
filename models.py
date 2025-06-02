from pydantic import BaseModel
from typing import List, Optional,Dict

class TweetSentiment(BaseModel):
    text: str
    label: str
    score: float

class SentimentResponse(BaseModel):
    summary: Dict[str, int]
    tweets: List[TweetSentiment]