import streamlit as st

# Title for the app
st.title("Generate a Podcast style dialogue")

# Input text box with label "Dialog"
user_input = st.text_input("Dialog", "")

# Processing the input by concatenating "_END"
if user_input:
    output = user_input + "_END"
    st.write("Output:", output)
