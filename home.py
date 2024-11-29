import streamlit as st
import openai
import requests
from typing import Dict
import pandas as pd

st.image("./images/logo.jpg", width=30)

# Streamlit App UI and Logic
st.title("Energize AI - Your personal energy assistant")

st.header("Customer support and service platform - Ask me anything about energy!")

# Set your API keys
OPENAI_API_KEY = st.secrets["openai"]["api_key"]

openai.api_key = OPENAI_API_KEY

# Function to interact with OpenAI's GPT models
def openai_chat(messages: Dict) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or gpt-3.5-turbo, etc.
        messages=messages
    )
    return response['choices'][0]['message']['content']

# Initialize session state for messages
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "OpenAI"  # Default model is OpenAI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input and generate response
if prompt := st.chat_input("What do you want to know about energy?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Initialize the response variable
    response = ""  # Default empty string for response in case no model is selected or an error occurs

    # Generate response based on the selected model
    if st.session_state.selected_model == "OpenAI (GPT-4)":
        # Make API call to OpenAI's GPT model
        response = openai_chat(st.session_state.messages)

    # Display assistant's response in chat
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Append assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
