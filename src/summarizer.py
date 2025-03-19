from src.sentiment import SentimentAnalyzer
from transformers import pipeline
import re
from huggingface_hub import login
from dotenv import load_dotenv
import os

hf_token = os.getenv("HF_TOKEN")
login(hf_token, add_to_git_credential=True)

class SentenceSummarizer(SentimentAnalyzer):
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initialize the summarization pipeline.
        """
        super().__init__()  # Initialize the parent class
        self.summarization_pipeline = pipeline("summarization", model=model_name)

    # def clean_text(self, text):
    #     """
    #     Clean the text by removing extra whitespace, special characters, and URLs.
    #     """
    #     text = re.sub(r'http\S+', '', text)  # Remove URLs
    #     text = re.sub(r'[^a-zA-Z0-9.,!?\'"\s]', '', text)  # Remove special characters
    #     text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    #     return text

    def summarize_text(self, article_content, min_length=50, max_length=150):
        """
        Summarize the given article content.
        """
        # Initialize the parent class
        cleaned_text = self.clean_text(article_content)
        summary = self.summarization_pipeline(cleaned_text, min_length=min_length, max_length=max_length)[0]
        return summary["summary_text"]

def text_summary(text: str, min_length: int = 50, max_length: int = 150,sentence_length:int=500):
    summarizer = SentenceSummarizer()
    text = text[:sentence_length]
    summary = summarizer.summarize_text(text, min_length, max_length)
    return summary

if __name__ == "__main__":
    text_summary()
