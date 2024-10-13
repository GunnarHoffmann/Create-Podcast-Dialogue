import streamlit as st
from google.cloud import texttospeech
from google.oauth2 import service_account

mykey = st.secrets["mykey"]

# Print loaded credentials to debug
#st.write(f"Using credentials from: {mykey}")

# Initialize Text-to-Speech client with the loaded credentials
client = texttospeech.TextToSpeechClient(credentials=mykey)

# Function to convert text to speech
def text_to_speech(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content

# Streamlit app
st.title("Google Text-to-Speech API Demo2")

input_text = st.text_area("Enter text to convert to speech", "Hello, this is a demo.")

text_to_speech("huhu")
