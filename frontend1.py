# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import requests
from datetime import datetime

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="LangGraph Agent UI", layout="wide")
st.title("MadhuKiran's AI Chatbot Agent")

# Keep chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")

    system_prompt = st.text_area(
        "System Prompt", 
        height=70, 
        placeholder="Define your AI Agent personality..."
    )

    provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

    MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    MODEL_NAMES_OPENAI = ["gpt-4.1"]

    if provider == "Groq":
        selected_model = st.selectbox("Groq Model:", MODEL_NAMES_GROQ)
    elif provider == "OpenAI":
        selected_model = st.selectbox("OpenAI Model:", MODEL_NAMES_OPENAI)

    allow_web_search = st.checkbox("🔎 Allow Web Search")
    st.markdown("---")
    st.button("🗑️ Clear Chat", on_click=lambda: st.session_state.messages.clear())

# ---------------- CHAT DISPLAY ----------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='background-color:#DCF8C6;padding:10px;border-radius:10px;margin:5px 0;text-align:right;'>"
                f"👤 <b>You:</b><br>{msg['content']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='background-color:#F1F0F0;padding:10px;border-radius:10px;margin:5px 0;text-align:left;'>"
                f"🤖 <b>Agent:</b><br>{msg['content']}</div>",
                unsafe_allow_html=True,
            )

# ---------------- CHAT INPUT ----------------
user_query = st.chat_input("Type your message...")

API_URL = "http://127.0.0.1:9999/chat"

if user_query:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Prepare payload for backend
    # payload = {
    #     "model_name": selected_model,
    #     "model_provider": provider,
    #     "system_prompt": system_prompt,
    #     "messages": [m["content"] for m in st.session_state.messages if m["role"] == "user"],
    #     "allow_search": allow_web_search,
    # }
    payload = {
    "model_name": selected_model,
    "model_provider": provider,
    "system_prompt": system_prompt,
    "messages": [user_query],   # 🚨 send ONLY the current query
    "allow_search": allow_web_search
}

    try:
        response = requests.post(API_URL, json=payload, timeout=60)

        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {response_data['error']}"})
            else:
                st.session_state.messages.append({"role": "assistant", "content": response_data})
        else:
            st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Error {response.status_code}"})
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Connection error: {e}"})

    st.rerun()
