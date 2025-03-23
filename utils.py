import os
import json
import re
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def clean_text(text):
    """
    Cleans the input text by removing special characters, multiple spaces, and newlines.
    """
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9.,!? ]', '', text)  # Keep alphanumeric and punctuation
    return text.strip()


def save_json(data, file_path):
    """
    Saves the given dictionary as a JSON file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    logging.info(f"Data saved to {file_path}")


def load_json(file_path):
    """
    Loads a JSON file and returns its content.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    logging.warning(f"File not found: {file_path}")
    return None


def save_audio(file_path, audio_data):
    """
    Saves an audio file in a specified directory.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as file:
        file.write(audio_data)
    logging.info(f"Audio file saved to {file_path}")

