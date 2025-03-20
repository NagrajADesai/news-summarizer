import os
import json
from dotenv import load_dotenv
from src.summarizer import text_summary

def analyze_news_sentiment(text):

    file_path = r"news-articles/ford_final_result.json"  # Use forward slashes

    # Read the JSON file
    with open(file_path, "r", encoding="utf-8") as file:
        all_articles = json.load(file)

    # Ensure 'Articles' key exists
    if "Articles" not in all_articles:
        raise KeyError("The key 'Articles' is missing from the JSON file.")

    # Build the formatted text correctly
    filtered_text = ''
    for i in all_articles["Articles"]:
        filtered_text += f"\n\nTitle: {i['title']}\nSummary: {i['summary']}\nSentiment: {i['sentiment']}"

    # Prompt for analysis
    prompt = filtered_text + """
        Your response should include:
        1. Overall Sentiment Distribution → Count how many articles are positive, negative, or neutral.
        2. Common Themes → Extract key topics from summaries.
        3. Sentiment Trends → Identify sentiment shifts across sources.
        4. Bias in Coverage → Identify if certain sources are more positive/negative.
        5. Key Insights → Provide a list of main takeaways.
        """

    print("the input text: ", prompt)  # Print for debugging or pass it to a model

    summary_text = text_summary(prompt)
    all_articles['Coverage differences'] = summary_text

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(all_articles, file, indent=4, ensure_ascii=False)
    
    print('*'*50)
    print("summary: ",summary_text)

# Example Usage (replace with your actual news article text)
if __name__ == '__main__':
    analyze_news_sentiment()
    