import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Speech-to-Text using OpenAI Whisper
def speech_to_text(audio_file_path):
    audio_file = open(audio_file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text'] if 'text' in transcript else "No transcription available."

# ✅ Text-to-Speech Placeholder (OpenAI doesn’t offer TTS yet)
# You can use Google Text-to-Speech or pyttsx3 (offline Python library)
def text_to_speech(text):
    return f"Text-to-Speech: {text} (OpenAI does not currently support TTS natively)"

# ✅ Image Analysis using OpenAI GPT-4 Vision (requires GPT-4V access)
# For now, we can use GPT-4 for text-based image description (upload image URL or image context)
def analyze_image(image_file_path):
    return "Image analysis via OpenAI requires GPT-4V access. Currently, use Google Vision API for image label detection."
