import streamlit as st
from api_handler import speech_to_text, text_to_speech, analyze_image
from database import init_db, save_transcript, get_all_transcripts

init_db()

st.set_page_config(page_title="Accessibility AI Tool", layout="wide")

st.title("Accessibility AI Tool")

tabs = st.tabs(["Speech-to-Text", "Text-to-Speech", "Image Analysis", "History"])

with tabs[0]:
    st.header("Speech-to-Text")
    audio_file = st.file_uploader("Upload an audio file for transcription", type=["wav", "mp3"])
    if audio_file is not None:
        with open("uploaded_audio.wav", "wb") as f:
            f.write(audio_file.read())
        transcription = speech_to_text("uploaded_audio.wav")
        st.write("### Transcription:", transcription)
        save_transcript(transcription)

with tabs[1]:
    st.header("Text-to-Speech")
    input_text = st.text_area("Enter text to convert to speech")
    if st.button("Convert to Speech"):
        speech_result = text_to_speech(input_text)
        st.write(speech_result)

with tabs[2]:
    st.header("Image Analysis")
    image_file = st.file_uploader("Upload an image for analysis", type=["jpg", "png"])
    if image_file is not None:
        with open("uploaded_image.png", "wb") as f:
            f.write(image_file.read())
        description = analyze_image("uploaded_image.png")
        st.write("### Image Description:", description)
        save_transcript(description)

with tabs[3]:
    st.header("Transcription and Image Analysis History")
    transcripts = get_all_transcripts()
    for t in transcripts:
        st.write(f"{t[0]}: {t[1]}")
