# news-summarizer

## 🛠️ Project Setup

1. **Create a Python environment:**

```bash
conda create -n venv python=3.11 -y
```

2. **Activate the environment:**

```bash
conda activate venv
```

3. **Install the required dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create .env file:**

create a .env file to store the api keys.

```bash
HF_TOKEN=<hugging-face-api-key>
```

# Project Structure

```
news-summarizer-tts/
│── src/
│   ├── __init__.py            # Marks the folder as a package
│   ├── helper.py              # Utility functions (reusable methods)
│   ├── news_scraper.py        # Extract news using BeautifulSoup
│   ├── summarizer.py          # Summarization logic using Hugging Face model
│   ├── sentiment.py           # Sentiment analysis logic
│   ├── tts_generator.py       # Convert summarized content into Hindi speech
│   ├── config.py              # Configuration settings (API keys, constants)
│
│── api/
│   ├── __init__.py            # Marks API as a package
│   ├── routes.py              # FastAPI routes for handling requests
│   ├── models.py              # Request and response models for API
│
│── ui/
│   ├── gradio_app.py          # Gradio-based UI for user interaction
│
│── research/
│   ├── trials.ipynb           # Experiments and research notebook
│
│── news-articles/             # scraped news saved in json file
│
│── .env                       # Environment variables (API keys, configurations)
│── requirements.txt            # List of dependencies
│── setup.py                    # Setup script (if needed for packaging)
│── app.py                      # Main entry point for FastAPI backend
│── README.md                   # Documentation for the project
│── huggingface.yml              # Hugging Face Spaces configuration file
│── runtime.txt                  # Python version for Hugging Face Spaces deployment

```
