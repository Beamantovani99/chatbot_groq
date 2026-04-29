from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

load_dotenv()

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Bea's Mario Chatbot",
    page_icon="🍄",
    layout="wide",
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>

/* Sfondo cielo Mario */
.stApp {
    background-image: url("https://i.imgur.com/8QfQKQp.png");
    background-size: cover;
}

/* Titolo stile pixel */
h1 {
    color: #ff0000;
    text-shadow: 3px 3px 0px #000;
    font-family: monospace;
}

/* Chat bubble utente */
[data-testid="stChatMessage"][data-testid*="user"] {
    background-color: #ffcc00;
    border: 3px solid #000;
    border-radius: 10px;
}

/* Chat bubble bot */
[data-testid="stChatMessage"][data-testid*="assistant"] {
    background-color: #00cc66;
    border: 3px solid #000;
    border-radius: 10px;
}

/* Input box */
textarea {
    border: 3px solid #000 !important;
    background-color: #fff8dc !important;
}

/* Bottone stile blocco Mario */
button {
    background-color: #ff0000 !important;
    color: white !important;
    border: 3px solid black !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("🍄 Super Mario Chatbot")

# ------------------ CHAT HISTORY ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    avatar = "🍄" if message["role"] == "assistant" else "🧑"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ------------------ MODEL ------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
)

# ------------------ INPUT ------------------
user_prompt = st.chat_input("💬 Scrivi qui...")

if user_prompt:
    st.chat_message("user", avatar="🧑").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = llm.invoke(
        input=[
            {"role": "system", "content": "Sei un assistente utile in stile Super Mario"},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant", avatar="🍄"):
        st.markdown(assistant_response)