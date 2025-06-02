import re

def clean_tweet(text: str) -> str:
    text = re.sub(r"http\S+", "", text)  
    text = re.sub(r"@\w+", "", text)     
    text = re.sub(r"#", "", text)        
    return text.strip()