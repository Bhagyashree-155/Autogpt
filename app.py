import streamlit as st
from agent import autogpt
from auth import login, signup

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Chatbot", layout="centered")

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat" not in st.session_state:
    st.session_state.chat = []

if "theme" not in st.session_state:
    st.session_state.theme = "dark"


# ---------------- THEME FUNCTION ----------------
def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #020617;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background-color: #f8fafc;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True)


apply_theme()


# ---------------- LOGIN / SIGNUP PAGE ----------------
if not st.session_state.logged_in:

    st.title("🔐 AI Chatbot Login")

    option = st.radio("Select Option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        if st.button("Create Account"):
            success, msg = signup(username, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    if option == "Login":
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")


# ---------------- CHATBOT PAGE ----------------
else:
    st.title("🚀 AI Chatbot with Memory + Context")

    # Top bar (theme + logout)
    col1, col2, col3 = st.columns([4, 1, 1])

    with col2:
        if st.button("🌓"):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()

    with col3:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.chat = []
            st.rerun()

    # Chat input
    user_input = st.chat_input("Ask anything...")

    if user_input:
        st.session_state.chat.append(("User", user_input))

        with st.spinner("Thinking..."):
            response = autogpt(user_input, st.session_state.chat)

        st.session_state.chat.append(("Bot", response))

    # Display chat messages
    for role, msg in st.session_state.chat:
        if role == "User":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)