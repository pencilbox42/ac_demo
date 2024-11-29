import streamlit as st
import openai
import requests
from typing import Dict
import pandas as pd

st.image("./images/logo.jpg", width=30)

# Streamlit App UI and Logic
st.title("Energize AI - Your energy assistant")

st.header("Ask me anything about energy!")


# Set your API key from Streamlit secrets
OPENAI_API_KEY = st.secrets["openai"]["api_key"]
openai.api_key = OPENAI_API_KEY

# Function to interact with OpenAI's GPT models
def get_openai_response(messages: list) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",  # You can change this to "gpt-3.5-turbo" if preferred
        messages=messages
    )
    return response['choices'][0]['message']['content']

# Initialize session state for messages if not already initialized
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
    response = get_openai_response(st.session_state.messages)

    # Display the assistant's response
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant's response in the chat window
    with st.chat_message("assistant"):
        st.markdown(response)
