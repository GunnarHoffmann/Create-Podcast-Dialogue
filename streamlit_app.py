import streamlit as st
import json
import os
from google.oauth2 import service_account
from google.cloud import texttospeech
from pydub import AudioSegment

# Title for the app
st.title("Generate a Podcast style dialogue")

# Input text box with label "Dialog"
user_input = st.text_area("Dialog", "", height=200)

# Define the speaker voices (you can use different voices for different speakers)
voice1 = "en-US-Journey-D"
voice2 = "en-US-Journey-F"

credentials_json = st.secrets["mykey"]
# st.write(credentials_json)
# Convert the string into a file-like object
credentials_info = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Print loaded credentials to debug
# st.write(f"Using credentials from: {mykey}")

# Initialize Text-to-Speech client with the loaded credentials
client = texttospeech.TextToSpeechClient(credentials=credentials)

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
        print(f'Audio content written to {foutput_filename}')
       
    #combined_audio = AudioSegment.from_mp3(output_filename)


def concatenate_audios(file_list, output_file):
    # Load the first audio file
    
    # Get the absolute path of the current directory
    current_directory = os.getcwd()

    # Create the full path to the file
    file_path = os.path.join(current_directory, file_list[0])
    combined_audio = AudioSegment.from_mp3(file_path)

    # Concatenate the rest of the audio files
    #for file in file_list[1:]:
    #    next_audio = AudioSegment.from_mp3(file)
    #    combined_audio += next_audio  # Concatenates the audio segments

    # Export the combined audio
    combined_audio.export(output_file, format="mp3")
    print(f"Combined audio saved as {output_file}")

# Processing the input by concatenating "_END"
if user_input:
    # Iterate through the text array and synthesize audio based on index
    for index, text in enumerate(texts):
        if index % 2 == 0:
            # Even index, use Speaker 1
            output_filename = f"output_speaker1_{index}.mp3"
            synthesize_text(text, voice1, output_filename)
            with open(f"output_speaker1_{index}.mp3", "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")
        else:
            # Odd index, use Speaker 2
            output_filename = f"output_speaker2_{index}.mp3"
            synthesize_text(text, voice2, output_filename)
            with open(f"output_speaker2_{index}.mp3", "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")

        # Add each generated file to the list for concatenation
        audio_files.append(output_filename)

        

    st.write(audio_files)

    from pydub.utils import which
    if which("ffmpeg") is not None:
        st.write("ffmpeg is installed.")
    else:
        st.write("ffmpeg is not installed or not in PATH.")
    
    # Concatenate all the generated audio files
    output_combined_file = "combined_output.mp3"
    #concatenate_audios(audio_files, output_combined_file)
    
    # After saving the audio file "test3.mp3"
    #with open("combined_output.mp3", "rb") as audio_file:
    #    st.audio(audio_file.read(), format="audio/mp3")
