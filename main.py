import streamlit as st
import openai
import requests
from typing import Dict

# Set your API keys
OPENAI_API_KEY = st.secrets["openai"]["api_key"]
ANTHROPIC_API_KEY = st.secrets["anthropic"]["api_key"]

openai.api_key = OPENAI_API_KEY

# Function to interact with OpenAI's GPT models
def openai_chat(messages: Dict) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or gpt-3.5-turbo, etc.
        messages=messages
    )
    return response['choices'][0]['message']['content']

# Function to interact with Anthropic's Claude models
def anthropic_chat(messages: Dict) -> str:
    # Anthropic API expects the "messages" parameter to be a single conversation history
    response = requests.post(
        "https://api.anthropic.com/v1/complete",
        headers={
            "Authorization": f"Bearer {ANTHROPIC_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "claude-2",  # Use Claude-1, Claude-2, or whichever model you want
            "prompt": "\n".join([msg["content"] for msg in messages]),
            "max_tokens": 150,
            "temperature": 0.7
        }
    )
    response_json = response.json()
    return response_json["completion"]

# Streamlit App UI and Logic
st.title("Energy Planner")
st.title("Ask me anything about energy!")

# Initialize session state for messages
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "OpenAI"  # Default model is OpenAI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Model selection dropdown
st.session_state.selected_model = st.selectbox(
    "Please select the model:",
    ["OpenAI (GPT-4)", "Anthropic (Claude-2)"]
)

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

    # Generate response based on the selected model
    with st.chat_message("assistant"):
        if st.session_state.selected_model == "OpenAI (GPT-4)":
            # Make API call to OpenAI's GPT model
            response = openai_chat(st.session_state.messages)
        elif st.session_state.selected_model == "Anthropic (Claude-2)":
            # Make API call to Anthropic's Claude model
            response = anthropic_chat(st.session_state.messages)

        # Display assistant's response in chat
        st.markdown(response)
    
    # Append assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
