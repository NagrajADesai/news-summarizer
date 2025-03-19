import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/news_scraper.py",
    "src/summarizer.py",
    "src/sentiment.py",
    "src/tts_generator.py",
    "src/config.py",
    "api/__init__.py",
    "api/routes.py",
    "api/models.py",
    "ui/gradio_app.py",
    "news_articles/__init__.py",
    "research/trials.ipynb",
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
    "README.md",
    "huggingface.yml",
    "runtime.txt"
]



for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")