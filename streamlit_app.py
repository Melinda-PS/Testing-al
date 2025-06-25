import streamlit as st
from api_handler import speech_to_text, text_to_speech, analyze_image
from database import init_db, save_transcript, get_all_transcripts

# Initialize database
init_db()

# Streamlit config
st.set_page_config(page_title="Accessibility AI Tool", layout="wide")

# Session states for accessibility settings
if 'font_size' not in st.session_state:
    st.session_state.font_size = 16
if 'high_contrast' not in st.session_state:
    st.session_state.high_contrast = False
if 'audio_feedback' not in st.session_state:
    st.session_state.audio_feedback = True

# Accessibility Sidebar
st.sidebar.header("Accessibility Settings")
st.sidebar.slider("Font Size", 12, 32, st.session_state.font_size, key='font_size')
high_contrast = st.sidebar.toggle("High Contrast Mode", value=st.session_state.high_contrast, key='high_contrast')
audio_feedback = st.sidebar.toggle("Audio Feedback", value=st.session_state.audio_feedback, key='audio_feedback')

st.sidebar.markdown("""
    ### Vision Support Features
    - Dyslexia-friendly fonts available
    - Color themes for different eye conditions
    - Large font sizes up to 32px
    - High contrast modes for low vision
""")

# Styling based on settings
font_size = f"{st.session_state.font_size}px"
contrast_style = "background-color: black; color: white;" if high_contrast else ""

def play_audio_feedback():
    if audio_feedback:
        st.markdown("""
            <audio autoplay>
                <source src="https://www.soundjay.com/buttons/sounds/button-3.mp3" type="audio/mpeg">
            </audio>
        """, unsafe_allow_html=True)

# Title Section
st.markdown(f"""
    <div style="font-size:{font_size}; {contrast_style}; padding: 10px; border-radius: 10px;">
        <h1>VoiceAccess AI</h1>
        <p>Transform your voice into accurate text with AI-powered accessibility features.</p>
    </div>
""", unsafe_allow_html=True)

# Main Tabs
tabs = st.tabs(["Speech-to-Text", "Text-to-Speech", "Image Analysis", "History"])

# Speech-to-Text Tab
with tabs[0]:
    st.markdown(f"<div style='font-size:{font_size}; {contrast_style};'><h2>Speech-to-Text</h2></div>", unsafe_allow_html=True)
    audio_file = st.file_uploader("Upload an audio file for transcription", type=["wav", "mp3"])

    if st.button("Transcribe Audio"):
        play_audio_feedback()
        if audio_file:
            with open("uploaded_audio.wav", "wb") as f:
                f.write(audio_file.read())
            transcription = speech_to_text("uploaded_audio.wav")
            st.markdown(f"<div style='font-size:{font_size}; {contrast_style};'><h3>Transcription:</h3><p>{transcription}</p></div>", unsafe_allow_html=True)
            save_transcript(transcription)
        else:
            st.warning("Please upload an audio file.")

# Text-to-Speech Tab
with tabs[1]:
    st.markdown(f"<div style='font-size:{font_size}; {contrast_style};'><h2>Text-to-Speech</h2></div>", unsafe_allow_html=True)
    input_text = st.text_area("Enter text to convert to speech")

    if st.button("Convert to Speech"):
        play_audio_feedback()
        if input_text:
            speech_result = text_to_speech(input_text)
            st.audio(speech_result)
        else:
            st.warning("Please enter text.")

# Image Analysis Tab
with tabs[2]:
    st.markdown(f"<div style='font-size:{font_size}; {contrast_style};'><h2>Image Analysis</h2></div>", unsafe_allow_html=True)
    image_file = st.file_uploader("Upload an image for analysis", type=["jpg", "png", "jpeg"])

    if st.button("Analyze Image"):
        play_audio_feedback()
        if image_file:
            with open("uploaded_image.png", "wb") as f:
                f.write(image_file.read())
            description = analyze_image("uploaded_image.png")
            st.markdown(f"<div style='font-size:{font_size}; {contrast_style};'><h3>Image Description:</h3><p>{description}</p></div>", unsafe_allow_html=True)
            save_transcript(description)
        else:
            st.warning("Please upload an image.")

# History Tab
with tabs[3]:
    st.markdown(f"<div style='font-size:{font_size}; {contrast_style};'><h2>Transcription and Image Analysis History</h2></div>", unsafe_allow_html=True)
    transcripts = get_all_transcripts()
    if transcripts:
        for t in transcripts:
            st.markdown(f"<div style='font-size:{font_size}; {contrast_style};'><p><b>{t[0]}:</b> {t[1]}</p></div>", unsafe_allow_html=True)
    else:
        st.info("No transcription or image analysis history found.")
