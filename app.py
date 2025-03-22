from src.news_scraper import main
from src.sentiment import text_sentiment
from src.summarizer import text_summary
from src.tts_generator import translate_and_speak
import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
import gradio as gr
import uvicorn

def create_json(company_name):
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
    else:
        output['Error'] = "Can't fetch the relevant information for the given information"
    
    return output


def summary_generation(output, company_name):
    filtered_text = ''
    for i in output['Articles']:
        filtered_text += i['title'] + " " + i['summary'] + " " +  i['sentiment']

    # add summary to the json file
    summary_text = text_summary(filtered_text)
    output['Coverage differences'] = summary_text

    os.makedirs("news_articles", exist_ok=True)
    json_file_path = os.path.join("news_articles", f"{company_name.lower()}.json")
    # # save the file
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)
        
    print(f"Articles saved to {json_file_path}")
    # convert englisgh to hindi and then save the mp3 file and save
    english_sentence = output['Coverage differences']
    translate_and_speak(english_sentence, company_name)

###### app creation


app = FastAPI()

class CompanyRequest(BaseModel):
    company_name: str

def get_company_info(company_name: str):

    # Get the directory of the current script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construct absolute paths using os.path.join
    json_file_path = os.path.join("news_articles", f"{company_name.lower()}.json")
    audio_file_path = os.path.join("audio_files", f"{company_name.lower()}.mp3")

    print(json_file_path)
    print(audio_file_path)
    
    json_output = {"error": "Company information not found."}
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as file:
            json_output = json.load(file)
    
    audio_output = None
    if os.path.exists(audio_file_path):
        audio_output = audio_file_path
    
    return json_output, audio_output

@app.post("/get_company_info")
def fetch_company_info(request: CompanyRequest):
    return get_company_info(request.company_name)

def create_gradio_app():
    title = "Company News summary & Hindi audio"
    description = "Enter a company name to fetch its news and an associated audio file."
    
    return gr.Interface(
        fn=get_company_info,
        inputs=gr.Textbox(label="Enter Company Name"),
        # outputs=[gr.Textbox(label="Company News Summary", interactive=False), gr.Audio(label="Summary news audio in Hindi")],
        outputs=[
        gr.JSON(label="Company News Summary"),
        gr.Audio(label="Summary news audio in Hindi")],
        title=title,
        description=description,
        flagging_mode='never'
    )


if __name__ == "__main__":

    # Create the Gradio interface
    demo = create_gradio_app()
    # Mount it to the FastAPI app
    app = gr.mount_gradio_app(app, demo, path="/")
    # Run the combined app
    uvicorn.run(app, host="0.0.0.0", port=8000)
