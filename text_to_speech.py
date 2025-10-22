import streamlit as st
from tts import TextToSpeech

txt2speech = TextToSpeech()

st.title('Text To Speech Example')

conversion_text = st.text_input('Text to convert', 'The quick brown fox jumps over the lazy dog')

if st.button('Convert'):
    txt2speech.convert(text=conversion_text)
    with open('hello.mp3', 'rb') as audio_file:
        audio_bytes = audio_file.read()

    st.audio(audio_bytes, format='audio/mp3')