import streamlit as st
from google.oauth2 import service_account
from google.cloud import texttospeech

# Title for the app
st.title("Generate a Podcast style dialogue")

# Input text box with label "Dialog"
user_input = st.text_area("Dialog", "", height=200)

# Define the speaker voices (you can use different voices for different speakers)
voice1 = "en-US-Journey-D"
voice2 = "en-US-Journey-F"

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'mykey.json'

# Load credentials directly from the service account key file
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

# Initialize Text-to-Speech client with the loaded credentials
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Print loaded credentials to debug
st.write(f"Using credentials from: {credentials.service_account_email}")

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

def synthesize_text2(text, speaker_name, output_filename):
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
    combined_audio = AudioSegment.from_mp3(file_list[0])

    # Concatenate the rest of the audio files
    for file in file_list[1:]:
        next_audio = AudioSegment.from_mp3(file)
        combined_audio += next_audio  # Concatenates the audio segments

    # Export the combined audio
    combined_audio.export(output_file, format="mp3")
    print(f"Combined audio saved as {output_file}")

text_to_speech("huhu")

# Processing the input by concatenating "_END"
if user_input:
    output = user_input + "_END"
    st.write("Output:", output)
    # Iterate through the text array and synthesize audio based on index
    for index, text in enumerate(texts):
        if index % 2 == 0:
            # Even index, use Speaker 1
            output_filename = f"output_speaker1_{index}.mp3"
            synthesize_text(text, voice1, output_filename)
        else:
            # Odd index, use Speaker 2
            output_filename = f"output_speaker2_{index}.mp3"
            synthesize_text(text, voice2, output_filename)

        # Add each generated file to the list for concatenation
        audio_files.append(output_filename)