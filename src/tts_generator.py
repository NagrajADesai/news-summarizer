import os
import soundfile as sf
from deep_translator import GoogleTranslator
from gtts import gTTS 


def text_to_speech_gtts(text, output_file="output.mp3"):
    tts = gTTS(text=text, lang="hi")
    tts.save(output_file)
    print(f"Speech saved as {output_file}")


class Translator:
    def translate_to_hindi(self, text):
        """
        Translate English text to Hindi.
        """
        return GoogleTranslator(source='en', target='hi').translate(text)

# Function to translate English text to Hindi and convert it to speech
def translate_and_speak(english_text, company_name):
    """
    Translate an English sentence to Hindi and convert it to speech.
    The audio file is saved in the specified directory.
    """
    # Ensure output directory exists
    output_dir = 'audio_files'
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize translator and TTS
    translator = Translator()
    
    # Translate text
    hindi_text = translator.translate_to_hindi(english_text)
    print(f"Translated Text: {hindi_text}")
    
    # Generate speech file path
    output_file = os.path.join(output_dir, f"{company_name.lower()}.mp3")
    
    # Convert text to speech
    text_to_speech_gtts(hindi_text, output_file)
    
    return output_file

# Example usage
if __name__ == "__main__":
    translate_and_speak()
   
