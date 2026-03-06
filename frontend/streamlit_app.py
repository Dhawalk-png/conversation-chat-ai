
import streamlit as st
import requests
import json
from typing import Optional

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.title(" AI Chatbot Assistant")

# Backend API configuration
BACKEND_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"
HEALTH_ENDPOINT = f"{BACKEND_URL}/health"
CLEAR_ENDPOINT = f"{BACKEND_URL}/clear-chat"

# Check backend health
@st.cache_resource
def check_backend_health():
    """Check if backend is running."""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=2)
        return response.status_code == 200
    except:
        return False

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

if "backend_available" not in st.session_state:
    st.session_state.backend_available = check_backend_health()

#sidebar
with st.sidebar:    
    st.header("Chatbot Settings")
    
    # Backend status
    if st.session_state.backend_available:
        st.success("✅ Backend Connected")
    else:
        st.error("❌ Backend Not Available")
        st.warning("Make sure FastAPI is running on http://localhost:8000")
    
    model = st.selectbox("select a model", ["gpt-3.5-turbo", "gpt-4"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    if st.button("clear chat history"):
        st.session_state.messages = []
        try:
            requests.post(CLEAR_ENDPOINT, timeout=5)
        except:
            pass

# Display chat messages
st.subheader("💬 Conversation")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input:
user_input = st.chat_input("type your message here...:")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message 
    with st.chat_message("user"):
        st.write(user_input)

    # Call FastAPI backend
    if st.session_state.backend_available:
        try:
            with st.spinner("Waiting for AI response..."):
                payload = {
                    "message": user_input,
                    "model": model,
                    "temperature": temperature
                }
                
                response = requests.post(CHAT_ENDPOINT, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    bot_response = data.get("assistant_message", "No response received")
                else:
                    bot_response = f"Error: {response.status_code} - {response.text}"
        
        except requests.exceptions.Timeout:
            bot_response = "⏱️ Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            bot_response = "🔌 Cannot connect to backend. Is FastAPI running on http://localhost:8000?"
            st.session_state.backend_available = False
        except Exception as e:
            bot_response = f"❌ Error: {str(e)}"
    else:
        bot_response = "❌ Backend is not available. Please start the FastAPI server."

    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    with st.chat_message("assistant"):
        st.write(bot_response)