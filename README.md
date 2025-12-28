# IST256 Chatapp

This is the code repository for building the IST256 AI Tutor. 

## What is it

This is a chatbot based on Open AI which is designed to function as an AI tutor for the IST256 course. The chatbot is designed to answer questions using the same style of python programming learned in the course. It will always explain any code it generates.

## Running

Run with Streamlit:

```bash
streamlit run app/chat/app.py
```

**Production (v2.0+):**
- `app/chat/app.py` - Main application with mode/context selection, user preferences, admin features

**Legacy (v1):**
- `app/chat/app_v1.py` - Original application (preserved for reference)

## Features (v2.0)

- **Mode Selection**: Tutor mode (guided learning) or Answer mode (direct solutions)
- **Context Injection**: Always-on assignment content loading for context-aware assistance
- **User Preferences**: Mode and context persist across sessions
- **Chat Logging**: All conversations logged to PostgreSQL database
- **Admin Features**: Settings, prompt editing, chat export (CSV/JSON), session debugging
- **Download History**: Users can download their chat sessions

