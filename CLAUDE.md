# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an AI tutoring chatbot for the IST256 Python programming course at Syracuse University. Built with Streamlit, it provides context-aware assistance using Azure OpenAI with RAG (Retrieval-Augmented Generation) to inject course assignment content into responses.

## Architecture

### Application Structure

```
app/
├── chat/              # Streamlit UI and chat logic
│   ├── app.py         # Main entry point - authentication, session, UI
│   ├── appnew.py      # New entry point being built out
│   ├── llmapi.py      # LLM client wrapper with conversation history
│   ├── ragapi.py      # RAG implementation (currently unused)
│   ├── docloader.py   # Loads assignment markdown from filecache
│   ├── constants.py   # UI text, icons, prompts, version
│   ├── settings.py    # Admin page for config management
│   ├── prompts.py     # Admin page for prompt editing
│   └── session.py     # Admin session debugging
├── llm/               # LLM backend implementations
│   ├── llmbase.py     # Abstract base class
│   ├── azureopenaillm.py  # Azure OpenAI integration
│   └── ollamallm.py   # Ollama local LLM integration
├── dal/               # Data Access Layer
│   ├── models.py      # Pydantic/SQLModel data models
│   ├── db.py          # PostgreSQL connection
│   └── s3.py          # MinIO S3 client
├── etl/               # Extract, Transform, Load pipeline
│   ├── run.py         # Main ETL orchestrator
│   ├── extract.py     # Downloads notebooks from GitHub
│   ├── transform.py   # Converts notebooks to markdown
│   ├── load.py        # (Unused) Would load to ChromaDB
│   └── filecache/     # Local markdown cache for assignments
├── data/              # Default configuration templates
│   ├── config.yaml    # Default AI model, temperature, system_prompt
│   └── prompts.yaml   # System prompt templates
├── chatlogger.py      # Logs chat messages to PostgreSQL
└── utils.py           # Email hashing, roster utilities
```

### Key Components

**Authentication Flow:**
1. User logs in via Azure AD (Microsoft MSAL)
2. Email validated against roster file in MinIO S3
3. Three user types: admin, exception (whitelist), roster
4. Session ID (UUID4) created per user

**Chat Flow:**
1. User selects assignment context (or "General Python")
2. Assignment markdown loaded from `app/etl/filecache/`
3. Context injected into system prompt using template in constants.py
4. User message → LLM API (with full conversation history)
5. Response streamed back to UI
6. Both user prompt and assistant response logged to PostgreSQL

**Configuration:**
- Runtime config stored in MinIO S3: `config.yaml` and `prompts.yaml`
- Admin users can modify via settings/prompts pages
- Changes persist to S3 and reload on next session

**RAG Implementation:**
- Assignment content injected as system message context (not vector search)
- All users currently get RAG enabled (experimental random assignment disabled)
- ChromaDB/vector search code exists but is commented out

### LLM Backend Strategy Pattern

The codebase uses the Strategy Pattern for LLM providers:
- `LLMBase` abstract class defines interface
- `AzureOpenAILLM` and `OllamaLLM` concrete implementations
- Switch via `LLM` environment variable ("azure" or "ollama")

Both implementations support:
- Streaming responses
- Message history management
- Temperature configuration

### Database Schema

PostgreSQL table `LogModel`:
- `sessionid` - User session UUID
- `userid` - User email
- `timestamp` - ISO format
- `model` - LLM model name used
- `rag` - Boolean (was RAG enabled?)
- `context` - Assignment name or "General Python"
- `role` - "user" or "assistant"
- `content` - Message text

## Development Commands

### Running the Application

**Local development:**
```bash
streamlit run app/chat/app.py
```

**Docker:**
```bash
docker-compose up
```

**ETL Pipeline** (refresh assignment documents):
```bash
python app/etl/run.py
```

### Testing

No test suite currently exists. Testing framework (pytest) is installed in requirements.txt but no test files are present.

### Environment Setup

1. Copy `.env.example` to `.env` (if exists) or create `.env` with required variables
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure PostgreSQL database is accessible
4. Ensure MinIO S3 has required files: `config.yaml`, `prompts.yaml`, roster file

## Critical Environment Variables

```bash
# LLM Configuration
LLM=azure                          # "azure" or "ollama"
AZURE_OPENAI_API_KEY=<key>
AZURE_OPENAI_ENDPOINT=https://ist256-openai-instance.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-08-01-preview
OLLAMA_HOST=https://ollama-proxy.cent-su.org

# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Authentication
MSAL_CLIENT_ID=<azure-ad-app-id>
MSAL_AUTHORITY=https://login.microsoftonline.com/<tenant-id>

# S3/MinIO Storage
S3_HOST=nas.home.michaelfudge.com:9000
S3_BUCKET=ist256chatapp
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=<secret>

# Files
LOCAL_FILE_CACHE=/workspaces/ist256-chatapp/app/etl/filecache
CONFIG_FILE=config.yaml
PROMPTS_FILE=prompts.yaml
ROSTER_FILE=ist256-fall2025-roster.txt

# Access Control
ADMIN_USERS=mafudge@syr.edu
ROSTER_EXCEPTION_USERS=email1@syr.edu,email2@syr.edu
```

## Important Files

- [app/chat/app.py](app/chat/app.py) - Main application entry point with authentication and UI
- [app/chat/llmapi.py](app/chat/llmapi.py) - Wrapper around LLM backends managing conversation history
- [app/chat/constants.py](app/chat/constants.py) - UI constants, RAG context templates, version
- [app/llm/azureopenaillm.py](app/llm/azureopenaillm.py) - Azure OpenAI implementation
- [app/dal/models.py](app/dal/models.py) - Data models for Auth, Configuration, Logs
- [app/etl/run.py](app/etl/run.py) - ETL pipeline that downloads and converts assignments

## Configuration Files

**app/data/config.yaml** (template, actual stored in MinIO S3):
```yaml
configuration:
  ai_model: gpt-5-nano
  system_prompt: learning     # "original" or "learning"
  temperature: 0.0
  whitelist: roster.txt
```

**app/data/prompts.yaml** (template, actual stored in MinIO S3):
```yaml
prompts:
  original: "Direct answer mode..."
  learning: "Socratic teaching mode..."
```

## System Prompts

Two teaching modes:
1. **original** - Fudgebot provides direct answers
2. **learning** - Socratic method, guides with questions

Selectable via admin settings page.

## Assignment Documents

Source: GitHub repository `ist256/spring2025`
- ETL pipeline downloads Jupyter notebooks from course repo
- Transforms to markdown, removes metacognition sections
- Stores in `app/etl/filecache/`
- 24 assignments total: Labs and HW for 12 topics (Intro through WebAPIs)

To update assignments: run `python app/etl/run.py`

## Admin Features

Admin users (defined in `ADMIN_USERS` env var) get sidebar access to:
- **Settings** - modify AI model, system prompt, temperature, roster file
- **Prompts** - edit system prompt templates
- **Session** - view session debug info

Changes persist to MinIO S3 and affect all users on next session.

## Deployment

### CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/build_and_publish.yaml`):
1. Triggers on push to `main` branch
2. Builds Docker image with Buildx
3. Pushes to GitHub Container Registry (ghcr.io)
4. Tags with `latest` and commit SHA
5. Updates separate `ist256-chatapp-deploy` repository
6. Triggers Kubernetes Helm deployment

### Docker Configuration

- Base image: `python:3.11`
- Entry point: `streamlit run --server.port $STREAMLIT_CHAT_APP_PORT /app/chat_app.py`
- Requires `.env` file mounted or environment variables set
- Exposes port defined in `STREAMLIT_CHAT_APP_PORT`

## Code Patterns

### Adding a New LLM Provider

1. Create new class in `app/llm/` inheriting from `LLMBase`
2. Implement `predict()` method (streaming and non-streaming)
3. Update `app/chat/llmapi.py` to instantiate your provider based on env var

### Adding a New Assignment

1. Add notebook path to `DOCUMENT_MANIFEST` in `app/etl/run.py`
2. Run ETL: `python app/etl/run.py`
3. Markdown file will appear in `app/etl/filecache/`
4. Update `app/chat/constants.py` `CONTEXTS` if display name needed

### Logging Custom Events

Use the `ChatLogger` instance:
```python
chat_logger.log_user_prompt(sessionid, email, context, text)
chat_logger.log_assistant_response(sessionid, email, context, text)
```

All logs go to PostgreSQL `LogModel` table.

## Important Notes

### Session State Management

Streamlit session state stores:
- `s3Client` - MinIO S3 client (singleton)
- `db` - PostgreSQL connection (singleton)
- `ai` - LLMAPI instance with conversation history
- `config` - ConfigurationModel from S3
- `prompts` - Prompts dictionary from S3
- `sessionid` - User session UUID
- `messages` - Streamlit chat message history
- `rag_context` - Current assignment markdown content

Clear session state by switching contexts or logging out.

### RAG Context Injection

Context template in [app/chat/constants.py:41-45](app/chat/constants.py):
```python
CONTEXT_CONTENT = """
You are in context: {context}

Here is the content:
{content}
"""
```

Assignment content injected as system message before user query.

### Authentication Edge Cases

- Users not on roster AND not in exception list are denied access
- Empty roster file treated as "allow all"
- Admin users bypass roster check

### Current Experimental Features

- Random RAG assignment via `hash_email_to_boolean()` - currently disabled (line 164 in app.py)
- ChromaDB vector search - code exists but commented out in `etl/load.py`
- Sentence transformers and LangChain imports commented out in requirements.txt

## Version Management

Version number stored in [app/chat/constants.py](app/chat/constants.py):
```python
VERSION = "0.3.0 (ui-upgrade)"
```

Update this when making releases. Version displayed in UI footer.
