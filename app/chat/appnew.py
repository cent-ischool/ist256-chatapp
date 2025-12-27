from add_parent_path import add_parent_path
add_parent_path(1)

import os
import random
from time import sleep
from uuid import uuid4
from datetime import datetime
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

def generate_chat_history_export() -> str:
    """
    Generates a formatted text export of the current chat session.

    Returns:
        Formatted string with session metadata and conversation history
    """
    lines = []
    lines.append("=" * 60)
    lines.append("IST256 AI Chat History")
    lines.append("=" * 60)
    lines.append(f"Session ID: {st.session_state.sessionid}")
    lines.append(f"User: {st.session_state.auth_model.email}")
    lines.append(f"Mode: {st.session_state.mode}")
    lines.append(f"Context: {st.session_state.context}")
    lines.append(f"Model: {st.session_state.config.ai_model}")
    lines.append(f"Export Time: {datetime.now().isoformat()}")
    lines.append("=" * 60)
    lines.append("")

    for idx, message in enumerate(st.session_state.messages, 1):
        role = message["role"].upper()
        content = message["content"]
        lines.append(f"[{idx}] {role}:")
        lines.append(content)
        lines.append("")
        lines.append("-" * 60)
        lines.append("")

    return "\n".join(lines)

def generate_all_chats_export() -> str:
    """
    Generates a formatted text export of all chat sessions for the current user.
    Queries the database to get all messages for this user.

    Returns:
        Formatted string with all chat sessions grouped by session ID
    """
    try:
        from sqlmodel import select
        from dal.models import LogModel

        # Query database for all user's messages using SQLModel
        with st.session_state.db.get_session() as session:
            statement = select(LogModel).where(
                LogModel.userid == st.session_state.auth_model.email
            ).order_by(LogModel.timestamp)

            results = session.exec(statement).all()

        if not results:
            return "No chat history found for this user."

        lines = []
        lines.append("=" * 60)
        lines.append("IST256 AI - Complete Chat History")
        lines.append("=" * 60)
        lines.append(f"User: {st.session_state.auth_model.email}")
        lines.append(f"Export Time: {datetime.now().isoformat()}")
        lines.append(f"Total Messages: {len(results)}")
        lines.append("=" * 60)
        lines.append("")

        # Group messages by session
        current_session = None
        message_num = 0

        for log in results:
            # New session header
            if log.sessionid != current_session:
                if current_session is not None:
                    lines.append("")
                    lines.append("=" * 60)
                    lines.append("")

                current_session = log.sessionid
                message_num = 0
                lines.append(f"SESSION: {log.sessionid}")
                lines.append(f"Started: {log.timestamp}")
                lines.append(f"Model: {log.model}")
                lines.append(f"Context: {log.context}")
                lines.append("-" * 60)
                lines.append("")

            # Message content
            message_num += 1
            lines.append(f"[{message_num}] {log.role.upper()}:")
            lines.append(log.content)
            lines.append("")

        lines.append("")
        lines.append("=" * 60)
        lines.append("End of Chat History")
        lines.append("=" * 60)

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"Failed to generate all chats export: user={st.session_state.auth_model.email}, error={e}")
        return f"Error generating chat history: {str(e)}"

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
                st.error(const.UNAUTHORIZED_MESSAGE)
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

    # ----------------- Sidebar: About & Help (v1.0.8) -----------------
    with st.expander("ℹ️ About & Help", expanded=False):
        st.markdown(const.ABOUT_PROMPT)
        st.markdown(const.TIPS_TEXT)
        st.markdown(const.FAQ_TEXT)




# ----------------- Load Up the Initial Session State -----------------
if 'file_cache' not in st.session_state:
    st.session_state.file_cache = FileCacheDocLoader(os.environ['LOCAL_FILE_CACHE'])
if "new_session_context" not in st.session_state:
    set_context("Tutor", "General Python")

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
        st.error("Unable to load Settings page. Try refreshing your browser. If the problem persists, contact mafudge@syr.edu.")
        logger.error(f"Failed to load Settings page: user={st.session_state.auth_model.email}, error={e}", exc_info=True)
elif current_page == "Prompts":
    try:
        from prompts import show_prompts
        logger.info(f"Admin user {st.session_state.auth_model.email} navigated to Prompts")
        show_prompts()
    except Exception as e:
        st.error("Unable to load Prompts page. Try refreshing your browser. If the problem persists, contact mafudge@syr.edu.")
        logger.error(f"Failed to load Prompts page: user={st.session_state.auth_model.email}, error={e}", exc_info=True)
elif current_page == "Session":
    try:
        from session import show_session
        logger.info(f"Admin user {st.session_state.auth_model.email} navigated to Session")
        show_session()
    except Exception as e:
        st.error("Unable to load Session page. Try refreshing your browser. If the problem persists, contact mafudge@syr.edu.")
        logger.error(f"Failed to load Session page: user={st.session_state.auth_model.email}, error={e}", exc_info=True)
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
            with st.spinner("Preparing your session..."):
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
        prompt = st.chat_input("Your message:")

        expander_text = f"AI Mode: `{st.session_state.mode}` Context: `{st.session_state.context}`"
        with st.expander(expander_text, expanded=False):
            mode = st.radio("Select AI Mode:", options=const.MODES, index=const.MODES.index(st.session_state.mode), horizontal=False, captions=const.MODE_CAPTIONS, help=const.MODE_HELP)
            context = st.selectbox("Chat About:", options=context_list, index=context_list.index(st.session_state.context), help=const.CONTEXT_HELP)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                set_mode = st.button("🔁 Save + New Chat", help="Switch chat context and mode. This will clear the chat history.")
            with col2:
                reset_to_defaults = st.button("♻️ Reset To Defaults", help="Reset chat settings to defaults. This will clear the chat history.")
            with col3:
                # Chat history download (v1.0.8)
                if len(st.session_state.messages) > 0:
                    chat_history_text = generate_chat_history_export()
                    st.download_button(
                        label="📥 Download Chat",
                        data=chat_history_text,
                        file_name=f"chat_history_{st.session_state.sessionid[:8]}.txt",
                        mime="text/plain",
                        help="Download this conversation as a text file"
                    )
                    logger.info(f"Chat history download button displayed: session={st.session_state.sessionid}, messages={len(st.session_state.messages)}")
                else:
                    st.button("📥 Download Chat", disabled=True, help="No messages to download yet")
            with col4:
                # Download all chats (v1.0.8)
                all_chats_text = generate_all_chats_export()
                st.download_button(
                    label="📥 Download All",
                    data=all_chats_text,
                    file_name=f"all_chats_{st.session_state.auth_model.email.split('@')[0]}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    help="Download all your chat sessions from the database"
                )
            if set_mode:
                set_context(mode, context)
                st.rerun()
            elif reset_to_defaults:
                set_context("Tutor", "General Python")
                st.rerun()

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
                    # Enhanced error handling with user-friendly messages (v1.0.8)
                    error_str = str(e).lower()
                    if "timeout" in error_str:
                        user_message = "The AI is taking longer than usual. Please try again in a moment."
                    elif "rate limit" in error_str or "429" in error_str:
                        user_message = "The AI service is busy. Please wait a moment and try again."
                    elif "connection" in error_str or "network" in error_str:
                        user_message = "Unable to connect to the AI service. Please check your connection and try again."
                    else:
                        user_message = "I'm having trouble responding right now. Please try rephrasing your question or try again in a moment."

                    st.error(user_message)
                    logger.error(f"LLM streaming error: model={st.session_state.config.ai_model}, mode={st.session_state.mode}, context={st.session_state.context}, error={e}")
                    # Add error to chat history so user sees it on rerun
                    st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {user_message}"})