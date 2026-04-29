from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

# load the env variables
load_dotenv()

# streamlit page setup
st.set_page_config(
    page_title="Bea's chatbot",
    page_icon="🤖",
    layout="wide",
)

# --- CUSTOM STYLE (rosa/viola) ---
st.markdown("""
    <style>
        /* Sfondo generale */
        body {
            background-color: #ffe6f2;
        }
        .stApp {
            background: linear-gradient(135deg, #ffd6f5, #f3c4ff, #e5b3ff);
        }

        /* Titolo */
        h1 {
            color: #b30086 !important;
            text-shadow: 1px 1px 2px #ffb3e6;
        }

        /* Chat bubbles */
        .stChatMessage {
            border-radius: 12px !important;
            padding: 12px !important;
        }

        /* Messaggi utente */
        .stChatMessage[data-testid="chat-message-user"] {
            background-color: #ffccf2 !important;
            border: 1px solid #ff99e6 !important;
        }

        /* Messaggi assistente */
        .stChatMessage[data-testid="chat-message-assistant"] {
            background-color: #f2ccff !important;
            border: 1px solid #d699ff !important;
        }

        /* Input box */
        .stChatInputContainer {
            background-color: #ffe6ff !important;
            border-radius: 10px !important;
            border: 2px solid #ffb3ff !important;
        }

        input[type="text"] {
            background-color: #fff0ff !important;
            color: #66004d !important;
        }
    </style>
""", unsafe_allow_html=True)

# Titolo
st.title("💬 Chatbot di IA Generativa")

# initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# llm initiate
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
)

# input box
user_prompt = st.chat_input("Chiedi al Chatbot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = llm.invoke(
        input=[{"role": "system", "content": "Sei un assistente utile"}, *st.session_state.chat_history]
    )
    assistant_response = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
