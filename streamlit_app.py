import streamlit as st
import json
import os
from google.oauth2 import service_account
from google.cloud import texttospeech
from pydub import AudioSegment
import docx2txt

st.image("brainlogo.png", width=100)
st.write("Powered by BRAIN Data Platform")

st.title("Generate a Podcast style dialogue")

# Define tabs
tabs = st.tabs(["Upload Input", "Configure TTS Engine", "Generate Output"])

with tabs[0]:
    st.header("Upload Input")
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = docx2txt.process(uploaded_file)
            st.write("File uploaded successfully.")
        elif uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")
            st.write("File uploaded successfully.")
        st.text_area("File Content:", text, height=200, readonly=True)

with tabs[1]:
    st.header("Configure TTS Engine")

with tabs[2]:
    st.header("Generate Output")
    # Create a button that triggers the info box
    # Initialize session state for managing the info box visibility
    if 'show_info' not in st.session_state:
        st.session_state['show_info'] = False

    # Button to toggle the info box visibility
    if st.button('How to create formatted input with a LLM'):
        # Toggle the value of 'show_info' in session state
        st.session_state['show_info'] = not st.session_state['show_info']

    # Display the info box based on the session state
    if st.session_state['show_info']:
        st.info('Sample prompt: Create a lively dialogue in podcast style about EON. Use attached file as input. Limit the output to maximum 50 lines. Create output as text array, each array entry equals to contribution of a speaker. Only two hosts shall discuss about the input. Do not add information about who is speaking, just add statements to array. Please introduce the members of the board of EON at the beginning. ')

    # Create a form with a text area and a submit button
    with st.form(key='text_area_form'):
        user_input = st.text_area("Text input:", '''[
    "Hm, have you seen the latest reports on Eon's fiscal year 2023?", 
    "Yes, the numbers are impressive! Revenue has increased by 15%.",   
    "Exactly, and that's mainly due to rising revenues from renewable energies.",  
    "Welll, that's really exciting! Eon seems to be adapting effectively to the shift towards green energy.",  
    "Absolutely, I'm curious to see how this will develop in the coming years!"   
]''', height=200)

        # Create an option box for 1st voice
        voice1selected = st.selectbox(
        'Select voice 1',
        ('en-US-Journey-D (male)', 'en-US-Journey-F (female)'),
        index=0
        )

        # Set the value of myvar based on the selected option
        if voice1selected == 'en-US-Journey-D (male)':
            voice1 = 'en-US-Journey-D'
        elif voice1selected == 'en-US-Journey-F (female)':
            voice1 = 'en-US-Journey-F'    

         # Create an option box for 2nd voice
        voice2selected = st.selectbox(
        'Select voice 2',
        ('en-US-Journey-D (male)', 'en-US-Journey-F (female)'),
        index=1
        )

        # Set the value of myvar based on the selected option
        if voice2selected == 'en-US-Journey-D (male)':
            voice2 = 'en-US-Journey-D'
        elif voice2selected == 'en-US-Journey-F (female)':
            voice2 = 'en-US-Journey-F'
        
        # Submit button
        submit_button = st.form_submit_button(label='Generate audio output using European Google TTS API endpoint')

    credentials_json = st.secrets["mykey"]
    # st.write(credentials_json)
    # Convert the string into a file-like object
    credentials_info = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    # Print loaded credentials to debug
    # st.write(f"Using credentials from: {mykey}")

    # Specify the European region endpoint
    client_options = {
        'api_endpoint': 'eu-texttospeech.googleapis.com:443'
    }

    # Initialize Text-to-Speech client with the loaded credentials
    client = texttospeech.TextToSpeechClient(credentials=credentials, client_options=client_options)

    # Define the text inputs in an array
    texts = [
        "Hum, Have you seen the latest reports on Eon's fiscal year 2023?",  # Even index (Speaker 1)
        "Yes, the numbers are impressive! Revenue has increased by 15%.",     # Odd index (Speaker 2)
        "Exactly, and that's mainly due to rising revenues from renewable energies.",    # Even index (Speaker 1)
        "That's really exciting! Eon seems to be adapting well to the shift towards green energy.",  # Odd index (Speaker 2)
        "Absolutely, I'm curious to see how this will develop in the coming years!",    # Even index (Speaker 1)
    ]

    # Store the output filenames to concatenate later
    audio_files = []

    # Function to convert text to speech
    def synthesize_text(text, speaker_name, output_filename):
        # Set the text input to be synthesized
        input_text = texttospeech.SynthesisInput(text=text)

        # Build the voice request based on the speaker
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=speaker_name,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )

        # Write the response to an MP3 file
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to {output_filename}')
           
    def concatenate_audios(file_list, output_file):
        # Load the first audio file
        
        # Create the full path to the file
        
        combined_audio = AudioSegment.from_mp3(file_list[0])

        # Concatenate the rest of the audio files
        for file in file_list[1:]:
            next_audio = AudioSegment.from_mp3(file)
            combined_audio += next_audio  # Concatenates the audio segments

        # Export the combined audio
        combined_audio.export(output_file, format="mp3")
        print(f"Combined audio saved as {output_file}")

    # Processing the input by concatenating "_END"
    if user_input:
        # Iterate through the text array and synthesize audio based on index
        try:
            inputarray = json.loads(user_input)    
            for index, text in enumerate(inputarray):
                if index % 2 == 0:
                    # Even index, use Speaker 1
                    output_filename = f"output_speaker1_{index}.mp3"
                    synthesize_text(text, voice1, output_filename)
                    #with open(f"output_speaker1_{index}.mp3", "rb") as audio_file:
                    #    st.audio(audio_file.read(), format="audio/mp3")
                else:
                    # Odd index, use Speaker 2
                    output_filename = f"output_speaker2_{index}.mp3"
                    synthesize_text(text, voice2, output_filename)
                    #with open(f"output_speaker2_{index}.mp3", "rb") as audio_file:
                    #    st.audio(audio_file.read(), format="audio/mp3")
        
                # Add each generated file to the list for concatenation
                audio_files.append(output_filename)
        
            # Concatenate all the generated audio files
            output_combined_file = "combined_output.mp3"
            concatenate_audios(audio_files, output_combined_file)
        
            #convert to m4a
            audio = AudioSegment.from_mp3("combined_output.mp3")
            audio.export("combined_output.wav", format="wav")
            
            # After saving the audio file "combined_output.mp3"
            with open("combined_output.mp3", "rb") as audio_file:
                st.write("Full dialogue in MP3 format:")
                st.audio(audio_file.read(), format="audio/mp3")

            # After saving the audio file "combined_output.mp3"
            with open("combined_output.wav", "rb") as audio_file:
                st.write("Full dialogue in WAV format:")
                st.audio(audio_file.read(), format="audio/wav")
                
        
        except:
            st.write('Error decoding input. Please use format as follows:')
            st.write('["Statement 1, Speaker 1", "Statement 1, Speaker 2", "Statement 2, Speaker 1", "Statement 2, Speaker 2"]')

        
        # Debug: generated files
        # st.write(audio_files)

        # Debug information
    from pydub.utils import which
    if which("ffmpeg") is not None:
      st.write("ffmpeg is installed.")
    else:
      st.write("ffmpeg is not installed or not in PATH.")
