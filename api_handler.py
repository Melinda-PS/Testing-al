# api_handler.py
import os
import openai
import base64
import requests
from dotenv import load_dotenv
from google.cloud import texttospeech

# Load API keys
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set Google Vision API Key
GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY")

# ✅ Speech-to-Text using OpenAI Whisper
def speech_to_text(audio_file_path):
    try:
        audio_file = open(audio_file_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript['text'] if 'text' in transcript else "No transcription available."
    except Exception as e:
        return f"Error transcribing audio: {e}"

# ✅ Text-to-Speech using Google Text-to-Speech API
def text_to_speech(text):
    try:
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        audio_file = "output.mp3"
        with open(audio_file, "wb") as out:
            out.write(response.audio_content)

        return audio_file

    except Exception as e:
        return f"Error generating speech: {e}"

# ✅ Image Analysis using Google Vision API
def analyze_image(image_file_path):
    try:
        url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"

        with open(image_file_path, "rb") as image_file:
            image_content = base64.b64encode(image_file.read()).decode('utf-8')

        payload = {
            "requests": [{
                "image": {"content": image_content},
                "features": [{"type": "LABEL_DETECTION", "maxResults": 5}]
            }]
        }

        response = requests.post(url, json=payload)
        result = response.json()

        labels = result['responses'][0]['labelAnnotations']
        description = ', '.join([label['description'] for label in labels])

        return description or "No labels found."

    except Exception as e:
        return f"Error analyzing image: {e}"
