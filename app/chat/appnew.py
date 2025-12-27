import os
import random
from time import sleep
from uuid import uuid4
import yaml

from loguru import logger
import streamlit as st
from streamlit_extras.bottom_container import bottom

from docloader import FileCacheDocLoader
import constants as const
from dal.s3 import S3Client
from dal.models import AuthModel, ConfigurationModel

def set_context(mode:str, context:str):
    # set new context
    # TODO Wrap in a model st.session_state.context_info = {
    st.session_state.new_session_context = True
    st.session_state.sessionid = str(uuid4())
    st.session_state.mode = mode
    st.session_state.context = context
    st.session_state.assistant_icon_offset = calculate_icon_offset(mode, context)
    st.session_state.context_injection = get_context_injection(context)

    # clear chat history / memory
    st.session_state.messages = [] # this is "ai.clear_history()"
    if 'ai' in st.session_state:
        st.session_state.ai.clear_history()

def calculate_icon_offset(mode, context):
    base_offset = 0 if mode == "Tutor" else 2
    if context != "General Python":
        base_offset +=1
    return base_offset

def get_context_injection(context: str) -> str:
    """Returns the context injection prompt based on the selected context."""
    if context != "General Python":
        content = st.session_state.file_cache.load_cached_document(context)
        return const.CONTEXT_PROMPT_TEMPLATE.format(assignment=context, content=content)
    else:
        return ""

def stream_text(text: str):
    """Streams text to the Streamlit chat message container."""
    for ch in text:
        yield ch
        sleep(random.uniform(0.001, 0.05))  # Simulate streaming delay     

# ----------------- Page And Sidebar Setup -----------------
# page config
st.set_page_config(
    page_title=const.TITLE, page_icon=const.LOGO, layout="centered", initial_sidebar_state="expanded", menu_items=None)

# hide streamlit menu
# st.markdown(const.HIDE_MENU_STYLE, unsafe_allow_html=True)

# logo
st.logo(const.LOGO)

# Sidebar
with st.sidebar as sidebar:
    st.title(const.TITLE)
    st.text(f"v{const.VERSION}",)

    # --- more to come here login and admin settings ---



# ----------------- Load Up the Initial Session State -----------------
if "new_session_context" not in st.session_state:
    set_context("Tutor", "General Python")
if 'file_cache' not in st.session_state:
    st.session_state.file_cache = FileCacheDocLoader(os.environ['LOCAL_FILE_CACHE'])

# set a multiline textbox preference
st.session_state.multiline_textbox = st.session_state.get("multiline_textbox", False)

# other preferences
context_list = ["General Python"]  + st.session_state.file_cache.get_doc_list()
expander_text = f"AI Mode: `{st.session_state.mode}`, Context: `{st.session_state.context}`"

# s3 client config
if 's3_client' not in st.session_state:
    s3_client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )
    st.session_state.s3_client = s3_client

# chat connfiguration based on settings
if 'config' not in st.session_state:
    config_yaml = st.session_state.s3Client.get_text_file(os.environ["S3_BUCKET"], os.environ["CONFIG_FILE"])
    prompts_yaml = st.session_state.s3Client.get_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"])
    config = ConfigurationModel.from_yaml_string(config_yaml)
    prompts = yaml.safe_load(prompts_yaml)['prompts']
    st.session_state.config = config
    st.session_state.system_prompt_text = prompts[config.system_prompt]


# ----------------- Chat Interface -----------------
avatars =  {
    'user': const.USER_ICON,
    'assistant': const.ASSISTANT_ICONS[st.session_state.assistant_icon_offset]
}

# shim the UI with some custom CSS for left/right chat message styles
st.markdown(const.CHAT_CONVERSATION_STYLE2,unsafe_allow_html=True)

#setup the initial AI context_message based on mode and context
if st.session_state.new_session_context:

    with st.chat_message("assistant", avatar=avatars["assistant"]):
        with st.spinner("Thinking..."):
            if st.session_state.mode == "Tutor":
                greeting = f"I am in Tutor mode. I  will provide guided learning for your {st.session_state.context} questions\n"
            else:
                greeting = f"I am in Answer mode. I will provide direct answers to your {st.session_state.context} questions\n"            
            st.write_stream(stream_text(greeting))

    st.session_state.new_session_context = False

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatars["user"] if message["role"] == "user" else avatars["assistant"]):
        st.markdown(message["content"])

# React to user input
#force these to the bottom of the page
with bottom():
    if st.session_state.multiline_textbox:
        prompt = st.text_area("Your message:", value="")
    else:
        prompt = st.chat_input("Your message:") 
    
    with st.expander(expander_text, expanded=False):
        mode = st.radio("Select AI Mode:", options=const.MODES, index=const.MODES.index(st.session_state.mode), horizontal=False, captions=const.MODE_CAPTIONS, help=const.MODE_HELP)
        context = st.selectbox("Chat About:", options=context_list, index=context_list.index(st.session_state.context), help=const.CONTEXT_HELP)
        col1, col2, col3 = st.columns([0.33, 0.33, 0.34])
        with col1:
            set_mode = st.button("🔁 Change Mode", help="Switch chat context and mode. This will clear the chat history.")
        with col2:
            reset_to_defaults = st.button("♻️ Reset To Defaults", help="Reset chat settings to defaults. This will clear the chat history.")
        if set_mode:
            set_context(mode, context)
            st.rerun()
        elif reset_to_defaults:
            set_context("Tutor", "General Python")
            st.rerun()
        with st.expander("⚙️ Settings", expanded=False):
            st.session_state.multiline_textbox = st.toggle("Multi-line Textbox", help="Choose between single-line and multi-line textbox for chat input.", value=st.session_state.get("multiline_textbox", False))
            st.write("TODO Download my chat history:")

# Take action on input
if prompt:
    # Display user message in chat message container
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        with st.spinner("Thinking..."):
            sleep(random.uniform(0.5, 3.5))  # Simulate thinking time
            response = f"What? {prompt} !?!?"
            st.write_stream(stream_text(response))
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})