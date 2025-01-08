# from  add_parent_path import add_parent_path
# add_parent_path(1)

import os 
import streamlit as st
from streamlit_msal import Msal

from ollamaapi import OllamaAPI
from dal.models import AuthModel


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
        subject = st.selectbox("Select a subject", ["Math", "Science", "English", "History"])
        st.write(auth_data)


if not auth_data:
    st.error(" ⬅️ Please sign in to continue.")
    st.stop()

#####################################
# Everything is a go!
if 'ai' not in st.session_state:
    ai = OllamaAPI(
        ollama_host=os.environ["OLLAMA_HOST"],
        model="dolphin3",
        system_prompt="You are a helpful AI assistant that speaks like a pirate."
    )
    st.session_state.ai = ai

st.markdown(
    """
<style>
    .st-emotion-cache-janbn0 {
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
""",
    unsafe_allow_html=True,
)

email = st.session_state.auth_model.email

st.logo("chat/images/ai-platform.svg")
st.write("The IST256 AI Tutor will launch soon.")
st.caption(f"Hey, {email} talking about {subject} today.")

# Display chat messages from history on app rerun
for message in st.session_state.ai.history[1:]:
    with st.chat_message(message["role"]): # <-- Inject avatar here
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.write_stream(st.session_state.ai.stream_response(prompt))
            # Add assistant response to chat history
            st.session_state.ai.record_response(response)