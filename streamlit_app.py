import streamlit as st

# Title for the app
st.title("Generate a Podcast style dialogue")

# Input text box with label "Dialog"
user_input = st.text_area("Dialog", "", height=200)

mykey = r"""{
  "type": "service_account",
  "project_id": "prj-mygcpproject-219-8a4e",
  "private_key_id": "a4bba25976599f38a3cf4b758f46fda6c3b25a71",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDB6vWKbGr8QSvm\naF4Ihb4tHNv0BdOWVFRQMldi0whcgwA40kMw/4xt7S+/9OBOcXX5Kl3Atd6LO4CY\nAjQPwpKo9BcgMF47+EfflF0dRN01PJ4E4RuUR893vdRwxCmfx9oV7CzXZLE4DI/K\nJ4gqZy9BsHwnlTsKDPScOo5dFNlKT4qLuK2B/FZWXVWGwkjwtdfqg+HxlBREmScT\nlVlHqxFBn6uldwSbWFsLqZRn3SH02EwjtjG93sl/3QVIEvaXmhvZ/76zOmiqdn35\n2MDPdM5T34Le4jkt9KAj1WJKAoYODbVxGtAzmijcRLoagaisNw44UUAeFUBddASj\nu0WuJ6FtAgMBAAECggEATuCFHtiJzfCubCqgsSPBnvUBrOkfzyKfJv3LGMoRORwa\nH4K7TPdthhs31INFJ/Mz0vV+LBBuJME/xdUDmzOAV1PuAixacFdF2PYux+SGfAyb\nlA2Cm9Z319Nx0aqg6bqvhUJLXRO6mDtX05kv5FuTV8tzPOCRIr3xU4jn9omv9u7d\nf/JY/AQQ0ZWcrz3sCPUH40/2zWAHYmSiQi58qNy4P4UZsCG1pFrVTSDacrw2Trv9\njrNc0eRw/7dNJZ893IND7o1Z8301MErWNDloH2Omv+2sQuKlPL6Fw1lnhAxOcL+G\niL3qzqCk0IDrx54gChmeruVLEsK5H4gkthyynBKsewKBgQDfvzpEwbiFQ8KvSeBF\nIHCghIOicswuEDWC1ehKiz68LyVDW+v7Kw78PBTQD/p5b67+PisjgIjA7BTWl0fg\nUFE8LewHp+odAbgcihK6P2BpWlPJGWXQT+p65zmSkgbY4OR2YbL/Jq8pWN1+uxsE\nI1qotl8W686RYzB1FKiUHEBaZwKBgQDd3veaf1iayKUa0sPvSGluk2H+fzDMZEfc\n0NRv+wJQy+GFVIo1Vuj9eOBQviKO6J6v+6GtDnlohvL2K82Vg9PUR5SevpxN0KoT\nEEDUTk8PRi+JdiKB1Qnxl2f/go1TNlA6bIxlJbgNms8c5+OG/1v88SDd658smwQM\nCM9leITpCwKBgE98bcTTVSvyoI0JH6UvGxPLP8BMLAEJPRlXyIgC46ySyxgc5b56\n034EEhjANGlDpdUoXMbl+K8gr150q9Iidll8ruchXegkHjX1TyXfMe77adx9K1BP\ns6spzagmPEx7yG3N03sVURDNQxKsgbJ8pM5ey3UnHGFF7YcKacEEMFBtAoGBAId8\nJI8/vIeohsn+co+oFFnlvi1+1fm6MvfwvgkzqpJULf8RROSVkelW6wPjV48VFfI5\nIt1evVzLK4qP7RakTbKPk33sv9300iaaAjyjJTwai+TRMvk9crkI0AUDX/G0dQF4\nT7NkeSQ1qMvp/tLtFOs9A+kAfU7rymje6Gb6VY9JAoGATSNskG2aLZQkZjtVU3kw\nLwB5y+DzXpLDEKzhbglTMAC/Qcgya6uxwyr66SmANwej9aUKdWQVYvrQZtpjPJJJ\nRr3L2oUIQEUnq7Mt3mFajpAXX+9bYRtxwEVY7r158Oi4gIdGpWjjr7PbPkw7DOZH\nNKG1gstcfOZ/uVosMTqRApo=\n-----END PRIVATE KEY-----\n",
  "client_email": "accessttsapi@prj-mygcpproject-219-8a4e.iam.gserviceaccount.com",
  "client_id": "110556404012116716347",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/accessttsapi%40prj-mygcpproject-219-8a4e.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}"""

# Open a file in write mode ('w') - this will create the file if it doesn't exist
with open("mykey.json", "w") as file:
    # Write the string to the file
    file.write(mykey)

from google.cloud import texttospeech

# Set the environment variable for authentication
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mykey.json"

# Initialize the Text-to-Speech client with the credentials
client = texttospeech.TextToSpeechClient()

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

# Processing the input by concatenating "_END"
if user_input:
    output = user_input + "_END"
    st.write("Output:", output)
