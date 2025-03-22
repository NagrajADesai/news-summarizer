import gradio as gr
import os
import json

def get_company_info(company_name):
    json_file_path = f"news-articles/ford_final_result.json"
    audio_file_path = f"audio_files/{company_name}.mp3"
    
    json_output = {"error": "Company information not found."}
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as file:
            json_output = json.load(file)
    
    audio_output = None
    if os.path.exists(audio_file_path):
        audio_output = audio_file_path
    
    return json.dumps(json_output, indent=4), audio_output



def create_gradio_app():
    title = "Company News summary & Hindi audio"
    description = "Enter a company name to fetch its news and an associated audio file."
    
    return gr.Interface(
        fn=get_company_info,
        inputs=gr.Textbox(label="Enter Company Name"),
        outputs=[gr.Textbox(label="Company News Summary", interactive=False), gr.Audio(label="Summary news audio in Hindi")],
        title=title,
        description=description,
        flagging_mode='never'
    )

if __name__ == "__main__":
    create_gradio_app()