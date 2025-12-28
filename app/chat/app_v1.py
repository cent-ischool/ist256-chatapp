# IST256 AI Tutor Chatbot - Legacy v1
# This file was the original app.py before v2.0.0
# Preserved for reference and emergency rollback
# DO NOT USE IN PRODUCTION - see app.py for current version

from  add_parent_path import add_parent_path
add_parent_path(1)

import os 
from loguru import logger
from uuid import uuid4
import yaml
import streamlit as st
from streamlit_msal import Msal

import constants as const 
from llmapi import LLMAPI
# from ragapi import RAGAPI
from docloader import FileCacheDocLoader
from utils import hash_email_to_boolean, get_roster
from llm.azureopenaillm import AzureOpenAILLM
from llm.ollamallm import OllamaLLM

from dal.chatlogger import ChatLogger
from dal.models import AuthModel, ConfigurationModel
from dal.db import PostgresDb
from dal.s3 import S3Client


def switch_context():
    logger.info(f"switching to context={st.session_state['context']}")
    #delete context_message
    del st.session_state['context_message']
    # clear chat history / memory
    if 'ai' in st.session_state:
        st.session_state.ai.clear_history()
    # create new user sesson id
    st.session_state.sessionid = str(uuid4())


# page config
st.set_page_config(
    page_title=const.TITLE, page_icon=const.LOGO, layout="centered", initial_sidebar_state="expanded", menu_items=None)

# hide streamlit menu
st.markdown(const.HIDE_MENU_STYLE, unsafe_allow_html=True)

# logo
st.logo(const.LOGO)

with st.sidebar as sidebar:
    st.title(const.TITLE)
    st.text(f"v{const.VERSION}",)

    auth_data = Msal.initialize_ui(
        client_id=os.environ["MSAL_CLIENT_ID"], 
        authority=os.environ["MSAL_AUTHORITY"],
        sign_out_label="Sign Out 🍊",
        disconnected_label="Sign In...",
        sign_in_label="SU Login 🍊"
    )

    if auth_data:
        # Not authorized yet?
        if 'validated' not in st.session_state or st.session_state.validated  not in ["roster", "exception"]:
            st.session_state.auth_data = auth_data
            st.session_state.auth_model = AuthModel.from_auth_data(auth_data)
            valid_users = get_roster(
                minio_host_port=os.environ["S3_HOST"],
                access_key=os.environ["S3_ACCESS_KEY"],
                secret_key=os.environ["S3_SECRET_KEY"],
                bucket_name=os.environ["S3_BUCKET"],
                object_key=os.environ["ROSTER_FILE"]
            )
            admin_users = [ user.lower().strip() for user in os.environ["ADMIN_USERS"].split(",") ]
            exception_users = [ user.lower().strip() for user in os.environ["ROSTER_EXCEPTION_USERS"].split(",") ]

            if st.session_state.auth_model.email in admin_users:
                st.session_state.validated = "admin"
            elif st.session_state.auth_model.email in exception_users:
                st.session_state.validated = "exception"
            elif st.session_state.auth_model.email in valid_users:
                st.session_state.validated = "roster"
            else: # Not allowed to be authorized
                st.error(f"🥺 '{st.session_state.auth_model.email}' is NOT listed on the class roster: '{os.environ['ROSTER_FILE']}' . If you feel this is error, please contact mafudge@syr.edu.")
                st.session_state.clear()
                st.stop()

        # You are now authorized
        st.session_state.file_cache = FileCacheDocLoader(os.environ['LOCAL_FILE_CACHE'])
        st.session_state.sessionid = str(uuid4()) if 'sessionid' not in st.session_state else st.session_state.sessionid
        context_list = ["General Python"]  + st.session_state.file_cache.get_doc_list()
        logger.info(f"docs_in_cache={st.session_state.file_cache.get_doc_list()}")

        logger.info(f"email={st.session_state.auth_model.email} validated={st.session_state.validated}, sessionid={st.session_state.sessionid}") 
        st.selectbox("Select a context", context_list, key="context", on_change=switch_context)
        logger.info(f"context={st.session_state.context}")
        with st.expander("‼️README‼️"):
            st.markdown(const.ABOUT_PROMPT)
            st.write(os.environ["ROSTER_FILE"])
            

    else: # Not authenticated
        st.markdown("### Welcome to the IST256 AI Tutor")
        st.info("Please sign with your SU credentials by clicking  the button above.")
        st.session_state.clear()
        st.stop()

    # Simple in-app navigation: Chat | Settings
    if st.session_state.validated == "admin":
        with st.expander("Admin Menu"):
            page = st.radio("Go to page", ["Chat", "Settings", "Prompts", "Session"], key="page_nav")
    else:
        page = "Chat"

#####################################
# Everything is a go. You are authenticated and authorized

if page == "Settings" and st.session_state.validated == "admin":
    import settings
    settings.show_settings()
    st.stop()

if page == "Prompts" and st.session_state.validated == "admin":
    import prompts
    prompts.show_prompts()
    st.stop()

if page == "Session" and st.session_state.validated == "admin":
    import session
    session.show_session()
    st.stop()

# ----------------- Load Up the Session State -----------------
if 's3Client' not in st.session_state:
    s3client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )
    st.session_state.s3Client = s3client

if 'config' not in st.session_state:
    config_yaml = st.session_state.s3Client.get_text_file(os.environ["S3_BUCKET"], os.environ["CONFIG_FILE"])
    prompts_yaml = st.session_state.s3Client.get_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"])
    config = ConfigurationModel.from_yaml_string(config_yaml)
    prompts = yaml.safe_load(prompts_yaml)['prompts']
    st.session_state.config = config
    st.session_state.system_prompt_text = prompts[config.system_prompt]

if 'db' not in st.session_state:
    db = PostgresDb(os.environ["DATABASE_URL"])
    st.session_state.db = db

if 'is_rag' not in st.session_state:
    # figure out if user is assgined to RAG for experiment
    # not really "rag" but injecting the context into the user prompt history.
    import random
    if st.session_state.validated == "exception" or st.session_state.validated == "admin":
        # always assign RAG to these users
        st.session_state.is_rag = True 
        # st.session_state.is_rag = random.choice([True, False])
        logger.info(f"rag={st.session_state.is_rag}, assignment=exception")
    else:
        # TODO: Make this a setting?
        # st.session_state.is_rag = hash_email_to_boolean(st.session_state.auth_model.email)
        # Override: always assign RAG to these users
        st.session_state.is_rag = True

        logger.info(f"rag={st.session_state.is_rag}, assignment=emailhash")

if 'ai' not in st.session_state:
    o_llm = OllamaLLM(
        host_url=os.environ["OLLAMA_HOST"],
        temperature=st.session_state.config.temperature, 
        model="dolphin3")
    a_llm = AzureOpenAILLM(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        model=st.session_state.config.ai_model,
        temperature=st.session_state.config.temperature
    )    
    
    if os.environ.get("LLM","azure") == "ollama":
        ai = LLMAPI(llm=o_llm, system_prompt=st.session_state.system_prompt_text)
        st.session_state.assistant_icon_offset = 2 + int(st.session_state.is_rag)
    else: # default is azure
        ai = LLMAPI(llm=a_llm, system_prompt=st.session_state.system_prompt_text)
        st.session_state.assistant_icon_offset = 0 + int(st.session_state.is_rag)
    st.session_state.ai = ai
    logger.info(f"env:LLM={os.environ.get('LLM')}, llm_model={st.session_state.ai._model}, temperature={st.session_state.ai._temperature}")
    logger.info(f"assistant_icon_offset={st.session_state.assistant_icon_offset}")

# ----------------- Chat Interface -----------------
# set the avatars
avatars =  {
    'user': const.USER_ICON,
    'assistant': const.ASSISTANT_ICONS[st.session_state.assistant_icon_offset]
}

# let's log what we havbe 
logger.info(f"avatars={avatars}")

# setup logger
chat_logger = ChatLogger(st.session_state.db, model=st.session_state.ai._model,rag=st.session_state.is_rag) 

# left/right chat windows
st.markdown(const.CHAT_CONVERSATION_STYLE,unsafe_allow_html=True)

email = st.session_state.auth_model.email
session = st.session_state.sessionid
context = st.session_state['context']

# Setup the context for "rag"
if 'context_message' not in st.session_state:
    st.session_state.context_message = True
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        with st.spinner("Thinking..."):
            greeting = f"Hi. My name is {st.session_state.auth_model.firstname}. Please rememeber it and call me by my on occasion.\n"
            if st.session_state['context'] != "General Python":
                if st.session_state.is_rag:
                    content = st.session_state.file_cache.load_cached_document(context)
                    context_message = greeting + \
                        const.CONTEXT_PROMPT_TEMPLATE.format(assignment=context, content=content)
                else:
                    context_message = greeting + \
                        const.CONTEXT_PROMPT_TEMPLATE_NO_CONTENT.format(assignment=context)
            else:
                context_message = greeting
            
        response = st.write_stream(st.session_state.ai.stream_response(context_message))

# Display chat messages from history on app rerun
for message in st.session_state.ai.history[2:]:
    with st.chat_message(message["role"], avatar=avatars[message['role']]): 
        st.markdown(message["content"])

# React to user input
if query := st.chat_input("Type in your question...", ):
    # Display user message in chat message container
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(query)

    # Display assistant response in chat message container
    # this is the main RAG algorithm... simple rag.
    with st.chat_message("assistant", avatar=avatars["assistant"], ):
        with st.spinner("Thinking..."):
            user_prompt = query
            chat_logger.log_user_prompt(session, email, context, user_prompt)
            response = st.write_stream(st.session_state.ai.stream_response(user_prompt))
            # Add assistant response to chat history
            chat_logger.log_assistant_response(session, email, context, response)
            st.session_state.ai.record_response(response)