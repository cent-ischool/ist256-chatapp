from add_parent_path import add_parent_path
add_parent_path(1)

import os
import random
from time import sleep
from uuid import uuid4
import yaml

from loguru import logger
import streamlit as st
from streamlit_extras.bottom_container import bottom
from streamlit_msal import Msal

from docloader import FileCacheDocLoader
import constants as const
from dal.s3 import S3Client
from dal.db import PostgresDb
from dal.models import AuthModel, ConfigurationModel
from chatlogger import ChatLogger
from utils import get_roster
from llm.azureopenaillm import AzureOpenAILLM
from llm.ollamallm import OllamaLLM
from llmapi import LLMAPI

def set_context(mode:str, context:str):
    # set new context
    # TODO Wrap in a model st.session_state.context_info = {
    st.session_state.new_session_context = True
    st.session_state.sessionid = str(uuid4())
    st.session_state.mode = mode
    st.session_state.context = context
    st.session_state.assistant_icon_offset = calculate_icon_offset(mode, context)

    # clear chat history / memory
    st.session_state.messages = [] # this is "ai.clear_history()"
    if 'ai' in st.session_state:
        st.session_state.ai.clear_history()
        # Apply context injection to system prompt based on mode and context
        if 'prompts' in st.session_state:
            mode_to_prompt_name = {"Tutor": "learning", "Answer": "original"}
            prompt_name = mode_to_prompt_name[mode]
            base_system_prompt = st.session_state.prompts[prompt_name]

            # Get context-enhanced system prompt
            enhanced_system_prompt = get_context_injection(context, base_system_prompt)
            st.session_state.ai.system_prompt = enhanced_system_prompt
            logger.info(f"System prompt updated: mode={mode}, context={context}")

def calculate_icon_offset(mode, context):
    base_offset = 0 if mode == "Tutor" else 2
    if context != "General Python":
        base_offset +=1
    return base_offset

def get_context_injection(context: str, system_prompt: str) -> str:
    """
    Returns enhanced system prompt with context injection if applicable.

    Args:
        context: The assignment context or "General Python"
        system_prompt: The base system prompt (from prompts.yaml based on mode)

    Returns:
        Complete system prompt with context prepended if applicable
    """
    if context != "General Python":
        try:
            content = st.session_state.file_cache.load_cached_document(context)
            context_injection = const.CONTEXT_PROMPT_TEMPLATE.format(
                assignment=context,
                content=content
            )
            logger.info(f"Context injected: {context}, size: {len(content)} chars")
            return context_injection + "\n\n" + system_prompt
        except FileNotFoundError:
            logger.error(f"Assignment file not found: {context}")
            st.warning(f"Assignment content for '{context}' is not available. Using general mode.")
            return system_prompt
        except Exception as e:
            logger.error(f"Error loading assignment {context}: {e}")
            st.warning(f"Unable to load assignment context. Please try again or select 'General Python'.")
            return system_prompt
    else:
        return system_prompt

def stream_text(text: str):
    """Streams text to the Streamlit chat message container."""
    def split_string_randomly(input_string):
        chunks = []
        while input_string:
            chunk_size = random.randint(2, 6)  # Random size between 2 and 5
            chunk = input_string[:chunk_size]  # Get the chunk
            chunks.append(chunk)  # Add it to the list
            input_string = input_string[chunk_size:]  # Remove the chunk from the input string
        return chunks    
    for chunk in split_string_randomly(text):
        yield chunk
        sleep(random.uniform(0.01, 0.1))  # Simulate streaming delay     


# ----------------- Page And Sidebar Setup -----------------
# page config
st.set_page_config(
    page_title=const.TITLE, page_icon=const.LOGO, layout="centered", initial_sidebar_state="expanded", menu_items=None)

# hide streamlit menu
# st.markdown(const.HIDE_MENU_STYLE, unsafe_allow_html=True)

# logo
st.logo(const.LOGO)

# ============= Sidebar =============
with st.sidebar:
    st.title(const.TITLE)
    st.text(f"v{const.VERSION}",)

    #  MSAL Authentication Widget
    auth_data = Msal.initialize_ui(
        client_id=os.environ["MSAL_CLIENT_ID"], 
        authority=os.environ["MSAL_AUTHORITY"],
        sign_out_label="Sign Out 🍊",
        disconnected_label="Sign In...",
        sign_in_label="SU Login 🍊"
    )

    # ----------------- Authentication Check  -----------------
    if auth_data:
        # Not authorized yet?
        if 'validated' not in st.session_state or st.session_state.validated  not in ["roster", "exception"]:
            st.session_state.auth_data = auth_data
            st.session_state.auth_model = AuthModel.from_auth_data(auth_data)
            # Load lists
            admin_users = [ user.lower().strip() for user in os.environ["ADMIN_USERS"].split(",") ]
            exception_users = [ user.lower().strip() for user in os.environ["ROSTER_EXCEPTION_USERS"].split(",") ]
            valid_users = [user.lower().strip() for user in get_roster(
                os.environ["S3_HOST"],
                os.environ["S3_ACCESS_KEY"],
                os.environ["S3_SECRET_KEY"],
                os.environ["S3_BUCKET"],
                os.environ["ROSTER_FILE"]
            )]
            # ----------------- Authorization -----------------
            email = st.session_state.auth_model.email
            # Validate user type
            if email in admin_users:
                st.session_state.validated = "admin"
            elif email in exception_users:
                st.session_state.validated = "exception"
            elif email in valid_users:
                st.session_state.validated = "roster"
            else:
                # ------------------ Unauthorized -----------------
                st.error(f"UNAUTHORIZED: '{email}' is NOT listed on the class roster: '{os.environ['ROSTER_FILE']}'. If you feel this is in error, please contact mafudge@syr.edu.")
                st.session_state.clear()
                st.stop()
    else: # Not authenticated
        st.info("Please sign with your SU credentials by clicking  the button above.")
        st.session_state.clear()
        st.stop()



    # ----------------- Sidebar: Admin Menu (v1.0.7) -----------------
    if 'validated' in st.session_state and st.session_state.validated == "admin":
        with st.expander("👔 Admin Menu", expanded=False):
            admin_page = st.radio(
                "Navigate to:",
                options=["Chat", "Settings", "Prompts", "Session"],
                index=0,
                help="Administrative pages for managing the chat application"
            )
            st.session_state.admin_page = admin_page
            logger.debug(f"Admin menu: page selected = {admin_page}")




# ----------------- Load Up the Initial Session State -----------------
if 'file_cache' not in st.session_state:
    st.session_state.file_cache = FileCacheDocLoader(os.environ['LOCAL_FILE_CACHE'])
if "new_session_context" not in st.session_state:
    set_context("Tutor", "General Python")

# set a multiline textbox preference
st.session_state.multiline_textbox = st.session_state.get("multiline_textbox", False)

# other preferences
context_list = ["General Python"]  + st.session_state.file_cache.get_doc_list()

# s3 client config
if 's3_client' not in st.session_state:
    s3_client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )
    st.session_state.s3_client = s3_client

# database connection
if 'db' not in st.session_state:
    # Strip quotes from DATABASE_URL if present (handles .env file format)
    db_url = os.environ["DATABASE_URL"].strip("'").strip('"')
    db = PostgresDb(db_url)
    st.session_state.db = db

# chat configuration based on settings
if 'config' not in st.session_state:
    config_yaml = st.session_state.s3_client.get_text_file(os.environ["S3_BUCKET"], os.environ["CONFIG_FILE"])
    prompts_yaml = st.session_state.s3_client.get_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"])
    config = ConfigurationModel.from_yaml_string(config_yaml)
    prompts = yaml.safe_load(prompts_yaml)['prompts']
    st.session_state.config = config
    st.session_state.prompts = prompts  # Store prompts in session state
    st.session_state.system_prompt_text = prompts[config.system_prompt]

# chat logger setup (prepared for v1.0.6)
if 'chat_logger' not in st.session_state:
    chat_logger = ChatLogger(
        st.session_state.db,
        model=st.session_state.config.ai_model,
        rag=True  # Always true in v2.0 (context always available)
    )
    st.session_state.chat_logger = chat_logger

# LLM backend initialization (v1.0.4)
if 'ai' not in st.session_state:
    try:
        # Mode-to-prompt mapping: Tutor uses Socratic "learning" prompt,
        # Answer uses direct "original" prompt
        mode_to_prompt_name = {"Tutor": "learning", "Answer": "original"}
        prompt_name = mode_to_prompt_name[st.session_state.mode]
        system_prompt = st.session_state.prompts[prompt_name]

        # Select backend based on LLM environment variable
        if os.environ["LLM"] == "azure":
            backend = AzureOpenAILLM(
                endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                api_key=os.environ["AZURE_OPENAI_API_KEY"],
                api_version=os.environ["AZURE_OPENAI_API_VERSION"],
                model=st.session_state.config.ai_model,
                temperature=st.session_state.config.temperature
            )
        else:  # ollama
            backend = OllamaLLM(
                host_url=os.environ["OLLAMA_HOST"],
                model=st.session_state.config.ai_model,
                temperature=st.session_state.config.temperature
            )

        # Initialize LLMAPI wrapper
        ai = LLMAPI(
            llm=backend,
            model=st.session_state.config.ai_model,
            temperature=st.session_state.config.temperature,
            system_prompt=system_prompt
        )
        st.session_state.ai = ai
        logger.info(f"Initialized LLM: backend={os.environ['LLM']}, model={st.session_state.config.ai_model}")

    except KeyError as e:
        st.error(f"Configuration error: Missing environment variable {e}")
        logger.error(f"Missing environment variable: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Failed to initialize LLM backend: {e}")
        logger.error(f"LLM initialization error: {e}")
        st.stop()


# ----------------- Page Routing (v1.0.7) -----------------
# Determine which page to display based on admin menu selection
current_page = st.session_state.get("admin_page", "Chat")

if current_page == "Settings":
    try:
        from settings import show_settings
        logger.info(f"Admin user {st.session_state.auth_model.email} navigated to Settings")
        show_settings()
    except Exception as e:
        st.error("Unable to load Settings page. Please contact support.")
        logger.error(f"Failed to load Settings page: {e}")
elif current_page == "Prompts":
    try:
        from prompts import show_prompts
        logger.info(f"Admin user {st.session_state.auth_model.email} navigated to Prompts")
        show_prompts()
    except Exception as e:
        st.error("Unable to load Prompts page. Please contact support.")
        logger.error(f"Failed to load Prompts page: {e}")
elif current_page == "Session":
    try:
        from session import show_session
        logger.info(f"Admin user {st.session_state.auth_model.email} navigated to Session")
        show_session()
    except Exception as e:
        st.error("Unable to load Session page. Please contact support.")
        logger.error(f"Failed to load Session page: {e}")
else:  # Chat (default page)
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
                # Get user's firstname with fallback
                firstname = st.session_state.auth_model.firstname if hasattr(st.session_state.auth_model, 'firstname') and st.session_state.auth_model.firstname else "Student"

                if st.session_state.mode == "Tutor":
                    greeting = f"Hello {firstname}! I am in Tutor mode. I will provide guided learning for your {st.session_state.context} questions.\n"
                else:
                    greeting = f"Hello {firstname}! I am in Answer mode. I will provide direct answers to your {st.session_state.context} questions.\n"
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

        expander_text = f"AI Mode: `{st.session_state.mode}` Context: `{st.session_state.context}`"
        with st.expander(expander_text, expanded=False):
            mode = st.radio("Select AI Mode:", options=const.MODES, index=const.MODES.index(st.session_state.mode), horizontal=False, captions=const.MODE_CAPTIONS, help=const.MODE_HELP)
            context = st.selectbox("Chat About:", options=context_list, index=context_list.index(st.session_state.context), help=const.CONTEXT_HELP)
            col1, col2, col3 = st.columns([0.33, 0.33, 0.34])
            with col1:
                set_mode = st.button("🔁 Change Mode / New Chat", help="Switch chat context and mode. This will clear the chat history.")
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

        # Log user prompt to database (v1.0.6)
        try:
            st.session_state.chat_logger.log_user_prompt(
                st.session_state.sessionid,
                st.session_state.auth_model.email,
                st.session_state.context,
                prompt
            )
            logger.debug(f"Logged user prompt: session={st.session_state.sessionid}, context={st.session_state.context}")
        except Exception as e:
            logger.error(f"Failed to log user prompt: {e}")

        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar=avatars["assistant"]):
            with st.spinner("Thinking..."):
                try:
                    # Stream response from LLM
                    response_stream = st.session_state.ai.stream_response(prompt)
                    full_response = st.write_stream(response_stream)

                    # Record response in conversation history
                    st.session_state.ai.record_response(full_response)

                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

                    # Log assistant response to database (v1.0.6)
                    try:
                        st.session_state.chat_logger.log_assistant_response(
                            st.session_state.sessionid,
                            st.session_state.auth_model.email,
                            st.session_state.context,
                            full_response
                        )
                        logger.debug(f"Logged assistant response: session={st.session_state.sessionid}, context={st.session_state.context}")
                    except Exception as log_error:
                        logger.error(f"Failed to log assistant response: {log_error}")

                except Exception as e:
                    error_message = f"I apologize, but I encountered an error: {str(e)}"
                    st.error(error_message)
                    logger.error(f"LLM streaming error: {e}")
                    # Add error to chat history so user sees it on rerun
                    st.session_state.messages.append({"role": "assistant", "content": error_message})