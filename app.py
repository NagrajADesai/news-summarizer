from src.news_scraper import main
from src.sentiment import text_sentiment
from src.summarizer import text_summary
from src.tts_generator import translate_and_speak
import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr
import uvicorn

# Ensure necessary directories exist
os.makedirs("news_articles", exist_ok=True)
os.makedirs("audio_files", exist_ok=True)

def create_json(company_name):
    output = {"Company": company_name}  # Store company name in output dictionary
    
    print('Start scraping data')
    result = main(company_name)  
    print('Done scraping data')

    if result:
        articles = []  # List to store article details
        count = 1

        for k, v in result.items():
            for info in v:
                title = info['title']
                content = info['content']
                complete_text = title + " " + content

                # Generate sentiment
                print(f'Generating sentiment result {count}')
                sentiment_result = text_sentiment(text=complete_text, sentence_length=200)

                # Generate summarization
                print(f'Generating summary {count}')
                text_sum = text_summary(complete_text, min_length= 50, max_length = 150, sentence_length=300)

                articles.append({
                    'title': title,
                    'summary': text_sum,
                    'sentiment': sentiment_result['sentiment']
                })

                count += 1
                if count > 10:
                    print('Breaking loop at count', count)
                    break

        output['Articles'] = articles
    else:
        output['Error'] = "Can't fetch the relevant information for the given company."

    return output


def summary_generation(output, company_name):
    filtered_text = ''
    for article in output.get('Articles', []):
        filtered_text += f"{article['title']} {article['summary']} {article['sentiment']} "

    # Generate summary
    summary_text = text_summary(filtered_text, min_length= 100, max_length = 300, sentence_length=1000)
    output['Coverage differences'] = summary_text
    print('done entire summary creation')

    # Save JSON file
    json_file_path = os.path.join("news_articles", f"{company_name.lower()}.json")
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)
    print('saved json file')

    print(f"Articles saved to {json_file_path}")

    # Convert English summary to Hindi audio
    translate_and_speak(summary_text, company_name)
    print('saved audio file')


def fetch_and_return_company_info(company_name: str):
    """Runs the JSON creation, summary generation, and returns output for Gradio."""
    print(f"Processing company: {company_name}")

    # Step 1: Create JSON
    output = create_json(company_name)

    # Step 2: Generate summary and save results
    summary_generation(output, company_name)

    # Step 3: Retrieve stored JSON and audio
    json_file_path = os.path.join("news_articles", f"{company_name.lower()}.json")
    audio_file_path = os.path.join("audio_files", f"{company_name.lower()}.mp3")

    json_output = {"error": "Company information not found."}
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as file:
            json_output = json.load(file)

    audio_output = audio_file_path if os.path.exists(audio_file_path) else None
    return json_output, audio_output


# FastAPI Application
app = FastAPI()

class CompanyRequest(BaseModel):
    company_name: str

@app.post("/get_company_info")
def fetch_company_info(request: CompanyRequest):
    return fetch_and_return_company_info(request.company_name)


def create_gradio_app():
    title = "Company News Summary & Hindi Audio"
    description = "Enter a company name to fetch its news summary and an associated audio file."

    return gr.Interface(
        fn=fetch_and_return_company_info,
        inputs=gr.Textbox(label="Enter Company Name"),
        outputs=[
            gr.JSON(label="Company News Summary"),
            gr.Audio(label="Summary News Audio in Hindi")
        ],
        title=title,
        description=description,
        flagging_mode='never'
    )


if __name__ == "__main__":
    demo = create_gradio_app()
    app = gr.mount_gradio_app(app, demo, path="/")
    uvicorn.run(app, host="0.0.0.0", port=8000)
