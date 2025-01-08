# from  add_parent_path import add_parent_path
# add_parent_path(1)

import os 
import streamlit as st
from streamlit_msal import Msal

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

# Everything is a go!
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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # call the LLM
    response = f"Echo: {prompt}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})