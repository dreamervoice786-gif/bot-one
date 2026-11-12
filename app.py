
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Nawash AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Purple theme
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1a1033, #3b1764, #241044);
    color: white;
}

section[data-testid="stSidebar"] {
    background: #170d2b;
}

.stChatMessage {
    background-color: rgba(255,255,255,0.08);
    border-radius: 12px;
}

h1, h2, h3, p, label {
    color: white !important;
}

.stButton button {
    background-color: #9333ea;
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton button:hover {
    background-color: #7e22ce;
}
</style>
""", unsafe_allow_html=True)


# Initialize Groq
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API key not found. Check your .env file.")
    st.stop()

client = Groq(api_key=api_key)


# Sidebar settings
with st.sidebar:
    st.title("⚙️ Settings")

    temperature = st.slider(
        "Temperature", 0.0, 2.0, 0.7, 0.1
    )

    max_tokens = st.slider(
        "Max Tokens", 256, 8192, 2048, 256
    )

    top_k = st.slider(
        "Top K", 1, 100, 40
    )

    top_p = st.slider(
        "Top P", 0.0, 1.0, 0.95, 0.05
    )

    st.caption(f"Selected Top K: {top_k}")
    st.caption("Powered by Groq API")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# Main interface
st.title("🤖 Nawash AI Chatbot")
st.caption("Powered by Groq | Qwen 3.8 27B")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
if prompt := st.chat_input("Ask me anything..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=st.session_state.messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stream=True
            )

            full_response = ""

            for chunk in response:
                content = chunk.choices[0].delta.content

                if content:
                    full_response += content
                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            response_placeholder.markdown(full_response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:
            st.error(f"API Error: {str(e)}")
