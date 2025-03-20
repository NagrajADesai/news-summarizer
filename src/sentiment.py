import re
import json
import os
import torch
from huggingface_hub import login
import re
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")
login(hf_token, add_to_git_credential=True)



class SentimentAnalyzer:
    def __init__(self, model_name="nlptown/bert-base-multilingual-uncased-sentiment"):
        """
        Initialize the sentiment analysis pipeline.
        """
        self.sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)

    def clean_text(self, text):
        """
        Clean the text by removing extra whitespace, special characters, and URLs.
        """
        text = text.lower()  # Convert to lowercase
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'[^a-zA-Z0-9.,!?\'\"\s]', '', text)  # Remove special characters
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
        return text

    def analyze_sentiment(self, article_content):
        """
        Analyze sentiment of the given article content and classify as positive, negative, or neutral.
        """
        cleaned_text = self.clean_text(article_content)
        result = self.sentiment_pipeline(cleaned_text)[0]
        
        # Map star ratings to sentiment categories
        star_rating = result["label"]
        
        if star_rating in ["5 stars", "4 stars"]:
            sentiment = "positive"
        elif star_rating in ["1 star", "2 stars"]:
            sentiment = "negative"
        else:  # 3 stars
            sentiment = "neutral"
        
        return {
            "original_label": result["label"],
            "score": result["score"],
            "sentiment": sentiment
        }

def text_sentiment(text:str, sentence_length:int=300):
    analyzer = SentimentAnalyzer()
    # keep the length of text less
    text = text[:sentence_length]
    results = analyzer.analyze_sentiment(text)
    return results

if __name__ == "__main__":
    text_sentiment()

    