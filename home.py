import streamlit as st
import openai
import requests
from typing import Dict
import pandas as pd

st.image("./images/logo.jpg", width=30)

# Streamlit App UI and Logic
st.title("Energize AI - Your personal energy assistant")

st.header("Ask me anything about energy!")


# Set your API key from Streamlit secrets
OPENAI_API_KEY = st.secrets["openai"]["api_key"]
openai.api_key = OPENAI_API_KEY

# Function to interact with OpenAI's GPT models (for openai==0.28)
def get_openai_response(prompt: str) -> str:
    # Use openai.Completion.create instead of ChatCompletion
    response = openai.Completion.create(
        model="text-davinci-003",  # Or another model of your choice (e.g., "curie", "babbage", etc.)
        prompt=prompt,
        max_tokens=150  # Limit the number of tokens in the response (adjust as needed)
    )
    return response['choices'][0]['text'].strip()

# Streamlit App UI
st.title("Energy Query Assistant")
st.write("Ask me anything about energy, solar power, or sustainability!")

# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input and generate response
prompt = st.text_input("What do you want to know about energy?")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response from OpenAI API
    response = get_openai_response(prompt)

    # Add assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant's response in the chat window
    with st.chat_message("assistant"):
        st.markdown(response)
