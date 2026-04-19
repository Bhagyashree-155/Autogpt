import streamlit as st
from agent import autogpt

st.title("🚀 AI Chatbot with Memory + Context")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.chat_input("Ask anything...")

if user_input:
    st.session_state.chat.append(("User", user_input))

    with st.spinner("Thinking..."):
        response = autogpt(user_input, st.session_state.chat)

    st.session_state.chat.append(("Bot", response))

# Display chat
for role, msg in st.session_state.chat:
    if role == "User":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)