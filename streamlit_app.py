# streamlit_app.py
import streamlit as st
from api_handler import speech_to_text, text_to_speech, analyze_image
from database import init_db, save_transcript, get_all_transcripts, get_transcripts_by_type, delete_transcript
import pandas as pd

init_db()

st.set_page_config(page_title="Accessibility AI Tool", layout="wide")

st.title("Accessibility AI Tool")

tabs = st.tabs(["Speech-to-Text", "Text-to-Speech", "Image Analysis", "History"])

# Speech-to-Text Tab
with tabs[0]:
    st.header("Speech-to-Text")
    audio_file = st.file_uploader("Upload an audio file for transcription", type=["wav", "mp3"])
    if audio_file is not None:
        with open("uploaded_audio.wav", "wb") as f:
            f.write(audio_file.read())
        transcription = speech_to_text("uploaded_audio.wav")
        st.write("### Transcription:", transcription)
        save_transcript(transcription, transcript_type="speech")

# Text-to-Speech Tab
with tabs[1]:
    st.header("Text-to-Speech")
    input_text = st.text_area("Enter text to convert to speech")
    if st.button("Convert to Speech"):
        if input_text:
            speech_result = text_to_speech(input_text)
            if speech_result:
                st.audio(speech_result, format="audio/mp3")
                save_transcript(input_text, transcript_type="speech")
            else:
                st.error("Failed to generate speech.")
        else:
            st.warning("Please enter text.")

# Image Analysis Tab
with tabs[2]:
    st.header("Image Analysis")
    image_file = st.file_uploader("Upload an image for analysis", type=["jpg", "png"])
    if image_file is not None:
        with open("uploaded_image.png", "wb") as f:
            f.write(image_file.read())
        description = analyze_image("uploaded_image.png")
        st.write("### Image Description:", description)
        save_transcript(description, transcript_type="image")

# History Tab
with tabs[3]:
    st.header("Transcription and Image Analysis History")

    filter_option = st.selectbox("Filter by type", ["All", "Speech", "Image"])

    if filter_option == "Speech":
        transcripts = get_transcripts_by_type("speech")
    elif filter_option == "Image":
        transcripts = get_transcripts_by_type("image")
    else:
        transcripts = get_all_transcripts()

    if transcripts:
        for t in transcripts:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.write(f"**{t[3]}** - *{t[2]}*")
                st.write(f"{t[1]}")
            with col2:
                if st.button("🗑️", key=f"delete_{t[0]}"):
                    delete_transcript(t[0])
                    st.experimental_rerun()

        if st.button("Export History to CSV"):
            df = pd.DataFrame(transcripts, columns=["ID", "Text", "Type", "Timestamp"])
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download CSV", data=csv, file_name='transcript_history.csv', mime='text/csv')
    else:
        st.info("No transcripts available.")
