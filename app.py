from src.news_scraper import main
from src.sentiment import text_sentiment
from src.summarizer import text_summary
from api.models import analyze_news_sentiment
from api.gradio_app import create_gradio_app
import re
import os
import json



def run_function(company_name):
    output = {}
    output['Company'] = company_name  # Store company name in output dictionary
    
    # Web scraping or data fetching function
    print('start scraping data')
    result = main(company_name)  
    print('done scraping data')

    count = 1
    if result:
        articles = []  # List to store article details

        for k, v in result.items():
            for info in v:
                title = info['title']
                content = info['content']
                complete_text = title + " " + content

                # Generate sentiment for the text
                print('generating sentiment result', count)
                sentiment_result = text_sentiment(text=complete_text, sentence_length=200)

                # Generate summarization
                print('generating summary', count)
                text_sum = text_summary(complete_text)

                # Append the dictionary to the articles list
                articles.append({
                    'title': title,
                    'summary': text_sum,
                    'sentiment': sentiment_result['sentiment']
                })
                # getting only 10 articles
                count += 1
                if count == 11:
                    print('breaking loop', count)
                    break
                else:
                    continue


        # Store all articles in the output dictionary
        output['Articles'] = articles
        # print(output)

    return output


# file_path = "D:\assignments\news-summarizer\news-articles\ford_final_result.json"  # Replace with your actual file path

# # Read the JSON file
# with open(file_path, "r", encoding="utf-8") as file:
#     all_articles = json.load(file)
# # all_articles = run_function('ford')
# filtered_text = ''
# for i in all_articles['Articles']:
#     filtered_text = i['title'] + " " + i['summary'] + " " +  i['sentiment']

# summary_text = text_summary(all_articles)




if __name__ == "__main__":

    # company = 'ford'
    # final_arr = run_function(company)
    # # save the result
    # output_dir = "news-articles"
    # file_path = os.path.join(output_dir, f"{company}_final_result.json")
    # with open(file_path, "w", encoding="utf-8") as f:
    #     json.dump(final_arr, f, indent=4, ensure_ascii=False)

    # print(final_arr)

    # generation summary for entire article
    # Corrected file path format

    ## audio file generator
    # file_path = r"news-articles/ford_final_result.json"  # Use forward slashes

    # # Read the JSON file
    # with open(file_path, "r", encoding="utf-8") as file:
    #     all_articles = json.load(file)

    # english_sentence = all_articles['Coverage differences']
    # translate_and_speak(english_sentence)

    create_gradio_app().launch()