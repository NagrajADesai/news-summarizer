from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from TTS.api import TTS
import soundfile as sf
from deep_translator import GoogleTranslator

class HindiTTS:
    def __init__(self, model_name="coqui_ai/vits_hi"):
        """
        Initialize the Text-to-Speech model for Hindi.
        """
        self.tts = TTS(model_name)

    def text_to_speech(self, text, output_file="output.wav"):
        """
        Convert Hindi text to speech and save as a WAV file.
        """
        audio_data = self.tts.tts(text)
        sf.write(output_file, audio_data, 22050)  # Save the audio file
        print(f"Speech saved as {output_file}")

class Translator:
    def translate_to_hindi(self, text):
        """
        Translate English text to Hindi.
        """
        translated_text = GoogleTranslator(source='en', target='hi').translate(text)
        return translated_text

