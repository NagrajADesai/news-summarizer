from src.news_scraper import main
from src.sentiment import text_sentiment
from src.summarizer import text_summary
from src.tts_generator import HindiTTS, Translator
import re
import json


# code for web scraping
company_name = 'nvidia'
result = main(company_name)

if result:

    # code for sentiment analysis

    output = {}
    # file_path = 'D:\\assignments\\news-summarizer\\news-articles\\nvidia_articles.json'

    with open(result, 'r', encoding='utf-8') as file:
        data = json.load(file)

    title = data['BBC'][1]['title']
    content = data['BBC'][1]['content']
    print(title)

    example = title + " " + content
    # result = text_sentiment(text=example,sentence_length=200)
    # output['title']= title 
    # output['sentiment'] = result['sentiment']
    # print(result)
    # print(f"output format {output}")


    # summarization
    # text_sum = text_summary(example)
    # output['summary'] = text_sum
    # print(output)



# Main Function: Summarize -> Translate -> Convert to Speech
# def summarize_translate_speak(text):

#     translator = Translator()
#     tts_model = HindiTTS()

#     # Step 1: Summarize in English
#     summary_english = text_sum
#     print("English Summary:", summary_english)

#     # Step 2: Translate to Hindi
#     summary_hindi = translator.translate_to_hindi(summary_english)
#     print("Hindi Translation:", summary_hindi)

#     # Step 3: Convert Hindi Text to Speech
#     tts_model.text_to_speech(summary_hindi)


# if __name__ == "__main__":
#     sample_text = """India is one of the largest democracies in the world. 
#     With a rich cultural heritage and diverse traditions, it has played a significant role in global history. 
#     Many technological advancements have emerged from India, shaping modern society."""
    
#     summarize_translate_speak(sample_text)