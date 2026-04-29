from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

# load the env variables
load_dotenv()

# streamlit page setup
st.set_page_config(
    page_title="Bea's chatbot",
    page_icon="🍄",
    layout="wide",
)

# ===== PIXEL FONT + MARIO STYLE =====
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">

<style>

/* ===== FONT PIXEL ===== */
html, body, [class*="css"]  {
    font-family: 'Press Start 2P', monospace;
}

/* ===== SFONDO MARIO PULITO ===== */
.stApp {
    background: linear-gradient(#5c94fc 70%, #c2f0ff 100%);
}

/* ===== TITOLO ===== */
h1 {
    color: #e52521;
    text-align: center;
    font-size: 18px;
    text-shadow: 2px 2px #000;
}

/* ===== CHAT BOX ===== */
[data-testid="stChatMessage"] {
    border: 3px solid black;
    border-radius: 4px;
    padding: 12px;
    margin-bottom: 12px;
    font-size: 10px;
    line-height: 1.6;
}

/* USER = coin */
[data-testid="stChatMessage"][aria-label="user"] {
    background-color: #ffd84d;
}

/* BOT = pipe */
[data-testid="stChatMessage"][aria-label="assistant"] {
    background-color: #5fd35f;
}

/* ===== INPUT ===== */
textarea {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 10px !important;
    border: 3px solid black !important;
    border-radius: 4px !important;
    background-color: #fff !important;
}

/* ===== INPUT CONTAINER ===== */
[data-testid="stChatInput"] {
    background-color: #ffffff;
    border-top: 4px solid black;
}

/* ===== SCROLLBAR RETRO ===== */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: black;
}

</style>
""", unsafe_allow_html=True)

st.title("🍄 SUPER MARIO CHATBOT")

# initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# show chat history
for message in st.session_state.chat_history:
    avatar = "🧑" if message["role"] == "user" else "🍄"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# llm initiate
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
)

# input box
user_prompt = st.chat_input("Scrivi...")

if user_prompt:
    st.chat_message("user", avatar="🧑").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = llm.invoke(
        input=[{"role": "system", "content": "Sei un assistente utile"}, *st.session_state.chat_history]
    )

    assistant_response = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant", avatar="🍄"):
        st.markdown(assistant_response)