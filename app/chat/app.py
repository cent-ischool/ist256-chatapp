from  add_parent_path import add_parent_path
add_parent_path(1)

import os 
from uuid import uuid4
import streamlit as st
from streamlit_msal import Msal

from constants import SYSTEM_PROMPT, ABOUT_PROMPT, CHAT_CONVERSATION_STYLE, HIDE_MENU_STYLE
from ollamaapi import OllamaAPI
from chatlogger import ChatLogger
from dal.models import AuthModel
from dal.db import PostgresDb

# hide streamlit menu
st.markdown(HIDE_MENU_STYLE, unsafe_allow_html=True)

# logo
st.logo("chat/images/ai-platform.svg")

with st.sidebar as sidebar:
    st.title("IST256 AI Tutor")

    auth_data = Msal.initialize_ui(
        client_id=os.environ["MSAL_CLIENT_ID"], 
        authority=os.environ["MSAL_AUTHORITY"],
        sign_out_label="Sign Out 🍊",
        disconnected_label="Sign In...",
        sign_in_label="SU Login 🍊"
    )

    if auth_data:
        st.session_state.auth_data = auth_data
        st.session_state.auth_model = AuthModel.from_auth_data(auth_data)
        st.session_state.sessionid = str(uuid4()) if 'sessionid' not in st.session_state else st.session_state.sessionid
        #subject = st.selectbox("Select a subject", ["Math", "Science", "English", "History"])
        with st.expander("❓About this app"):
            st.markdown(ABOUT_PROMPT)
            #st.write(auth_data)

if not auth_data:
    st.markdown("### Welcome to the IST256 AI Tutor")
    st.info("⬅️ Please sign with your SU credentials by clicking `>` next to the logo.")
    st.session_state.clear()
    st.stop()



#####################################
# Everything is a go!
   
if 'db' not in st.session_state:
    db = PostgresDb(os.environ["DATABASE_URL"])
    st.session_state.db = db

if 'ai' not in st.session_state:
    ai = OllamaAPI(
        ollama_host=os.environ["OLLAMA_HOST"],
        model="dolphin3",
        system_prompt=SYSTEM_PROMPT
    )
    st.session_state.ai = ai

avatars =  {
    'user': "chat/images/question.svg",
    'assistant': "chat/images/ai-platform.svg",
}

logger = ChatLogger(st.session_state.db)


# left/right chat windows
st.markdown(CHAT_CONVERSATION_STYLE,unsafe_allow_html=True)

email = st.session_state.auth_model.email
session = st.session_state.sessionid

#st.write(f"Hey, {email} talking about {subject} today.")

if 'first_message' not in st.session_state:
    st.session_state.first_message = True
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        with st.spinner("Thinking..."):
            first_message = f"Hi. My name is {st.session_state.auth_model.firstname}."
            response = st.write_stream(st.session_state.ai.stream_response(first_message))

# Display chat messages from history on app rerun
for message in st.session_state.ai.history[2:]:
    with st.chat_message(message["role"], avatar=avatars[message['role']]): 
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("Type in your question..."):
    # Display user message in chat message container
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        with st.spinner("Thinking..."):
            logger.log_user_prompt(session, email, prompt)
            response = st.write_stream(st.session_state.ai.stream_response(prompt))
            # Add assistant response to chat history
            logger.log_assistant_response(session, email, response)
            st.session_state.ai.record_response(response)