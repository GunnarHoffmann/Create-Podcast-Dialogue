import streamlit as st
import json
import os
from google.oauth2 import service_account
from google.cloud import texttospeech
from pydub import AudioSegment
import docx2txt
import requests

st.image("brainlogo.png", width=100)
st.write("Powered by BRAIN Data Platform")

st.title("Generate a Podcast style dialogue")

# Define tabs
tabs = st.tabs(["Upload Input", "Configure TTS Engine", "Generate Audio"])

with tabs[0]:
    st.header("Upload Input")
    st.info("""ℹ️ The word document should contain a dialogue format that clearly distinguishes between speakers. For example: \n\n- Emma: Hey, did you finish the report for the meeting?
\n- James: Not yet. I’m still working on the charts. What about you?
\n- Emma: I wrapped it up last night. Want me to take a look at yours?
\n- James: That’d be great. I’m stuck on the sales data comparison.""")
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = docx2txt.process(uploaded_file)
            st.write("File uploaded successfully.")
        elif uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")
            st.write("File uploaded successfully.")
        st.text_area("File Content:", text, height=200, disabled=True)

with tabs[1]:
    st.header("Configure TTS Engine")
    # Add a radio button to select between Google TTS and ElevenLabs TTS
    tts_engine = st.radio("Select TTS Engine", ("ElevenLabs TTS", "Google TTS"), key='tts_engine_selection', index=0)

    # Depending on the selected TTS engine, provide different voice options
    if tts_engine == "Google TTS":
        voice1selected = st.selectbox(
            'Select voice 1',
            ('en-US-Journey-D (male)', 'en-US-Journey-F (female)'),
            index=0
        )
        voice2selected = st.selectbox(
            'Select voice 2',
            ('en-US-Journey-D (male)', 'en-US-Journey-F (female)'),
            index=1
        )
    elif tts_engine == "ElevenLabs TTS":
        # Fetch available voices from ElevenLabs API
        elevenlabs_api_key = st.secrets["elevenlabs_api_key"]
        headers = {"xi-api-key": elevenlabs_api_key}
        response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)

        if response.status_code == 200:
            voices = response.json()["voices"]
            voice_names = [voice["name"] for voice in voices]
            
            voice1selected = st.selectbox('Select voice 1', voice_names, index=0)
            voice2selected = st.selectbox('Select voice 2', voice_names, index=1)
        else:
            st.error("Failed to fetch voices from ElevenLabs. Please check your API key and connection.")

with tabs[2]:
    st.header("Generate Audio")

    # Add info box
    st.info("""ℹ️ Podcasts can be created using two approaches. You can provide a pre-written script, and the podcast will be developed based on your content. Alternatively, you can share a prompt, and an advanced language learning model (LLM) will generate the script for you.""")

    # Add radio buttons to select between script-based or LLM prompt-based audio creation
    audio_creation_method = st.radio("Select Audio Creation Method", ("Audio creation based on script", "Audio creation based on LLM prompt"), index=0)

    if audio_creation_method == "Audio creation based on script" and uploaded_file is not None:
        # Create a form with a text area and a submit button
        with st.form(key='text_area_form'):
            user_input = st.text_area("Text input:", '''[
    "Hm, have you seen the latest reports on Eon's fiscal year 2023?", 
    "Yes, the numbers are impressive! Revenue has increased by 15%.",   
    "Exactly, and that's mainly due to rising revenues from renewable energies.",  
    "Well, that's really exciting! Eon seems to be adapting effectively to the shift towards green energy.",  
    "Absolutely, I'm curious to see how this will develop in the coming years!"   
]''', height=200)
            
            # Submit button
            submit_button = st.form_submit_button(label='Generate audio output using selected TTS API endpoint')

    elif audio_creation_method == "Audio creation based on LLM prompt":
        user_input = st.text_area("LLM Prompt:", "Create BLA BLA ...", height=200)
        submit_button = st.button(label='Generate audio output using selected TTS API endpoint')

    credentials_json = st.secrets["mykey"]
    credentials_info = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    client_options = {
        'api_endpoint': 'eu-texttospeech.googleapis.com:443'
    }

    client = texttospeech.TextToSpeechClient(credentials=credentials, client_options=client_options)

    audio_files = []

    def synthesize_text_google(text, speaker_name, output_filename):
        # Set the value of voice based on the selected option
        if speaker_name == 'en-US-Journey-D (male)':
            voice_name = 'en-US-Journey-D'
        elif speaker_name == 'en-US-Journey-F (female)':
            voice_name = 'en-US-Journey-F'

        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to {output_filename}')

    def synthesize_text_elevenlabs(text, voice_id, output_filename):
        elevenlabs_api_key = st.secrets["elevenlabs_api_key"]
        headers = {
            "xi-api-key": elevenlabs_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "voice_id": voice_id,
            "format": "mp3"
        }
        response = requests.post("https://api.elevenlabs.io/v1/text-to-speech", headers=headers, json=payload)
        if response.status_code == 200:
            with open(output_filename, "wb") as out:
                out.write(response.content)
                print(f'Audio content written to {output_filename}')
        else:
            st.error("Failed to generate audio with ElevenLabs TTS. Please check your API key and connection.")

    def concatenate_audios(file_list, output_file):
        combined_audio = AudioSegment.from_mp3(file_list[0])
        for file in file_list[1:]:
            next_audio = AudioSegment.from_mp3(file)
            combined_audio += next_audio
        combined_audio.export(output_file, format="mp3")
        print(f"Combined audio saved as {output_file}")

    if 'user_input' in locals() and user_input:
        try:
            inputarray = json.loads(user_input)
            for index, text in enumerate(inputarray):
                output_filename = f"output_speaker_{index}.mp3"
                if tts_engine == "Google TTS":
                    if index % 2 == 0:
                        synthesize_text_google(text, voice1selected, output_filename)
                    else:
                        synthesize_text_google(text, voice2selected, output_filename)
                elif tts_engine == "ElevenLabs TTS":
                    voice_id = voice1selected if index % 2 == 0 else voice2selected
                    synthesize_text_elevenlabs(text, voice_id, output_filename)
                audio_files.append(output_filename)
            output_combined_file = "combined_output.mp3"
            concatenate_audios(audio_files, output_combined_file)
            audio = AudioSegment.from_mp3("combined_output.mp3")
            audio.export("combined_output.wav", format="wav")
            with open("combined_output.mp3", "rb") as audio_file:
                st.write("Full dialogue in MP3 format:")
                st.audio(audio_file.read(), format="audio/mp3")
            with open("combined_output.wav", "rb") as audio_file:
                st.write("Full dialogue in WAV format:")
                st.audio(audio_file.read(), format="audio/wav")
        except:
            st.write('Error decoding input. Please use format as follows:')
            st.write('["Statement 1, Speaker 1", "Statement 1, Speaker 2", "Statement 2, Speaker 1", "Statement 2, Speaker 2"]')

    from pydub.utils import which
    if which("ffmpeg") is not None:
        st.write("ffmpeg is installed.")
    else:
        st.write("ffmpeg is not installed or not in PATH.")
