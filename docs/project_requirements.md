# Project Requirements

This document tracks high-level feature requirements for the IST256 Chatapp organized by version.

## Version Guidelines

- **Major version** (x.0.0): Breaking changes, major architectural shifts
- **Minor version** (1.x.0): New features, backward compatible
- **Patch version** (1.0.x): Bug fixes, minor improvements

---

## v1.0.1

**Status**: Released
**Release Date**: 2025-01-15

### Features

- Added "Session" page to admin menu to view session variables
- Added version number constant in constants.py
- Version number displayed in the app footer of the sidebar

### Technical Notes

- Simple implementation, no database changes
- UI-only feature using Streamlit
- Admin-only access via user type check

---

## v1.0.2

**Status**: Planned
**Release Date**: TBD

### Features

- MSAL authentication integration in appnew.py
- Roster/whitelist validation (admin, exception, roster users)
- User type detection and storage in session state
- Error handling for unauthorized users

### Technical Notes

- Port authentication from app.py to appnew.py (lines 50-82)
- Uses existing authentication patterns
- Environment variables: MSAL_CLIENT_ID, MSAL_AUTHORITY, ADMIN_USERS, ROSTER_EXCEPTION_USERS
- Foundation for v2.0 new UI
- Complexity: Medium | Effort: 4-6 hours

---

## v1.0.3

**Status**: Planned
**Release Date**: TBD

### Features

- PostgreSQL database connection initialization
- ChatLogger instance creation
- Session ID tracking with user metadata
- Prepare logging infrastructure for future use

### Technical Notes

- Initialize PostgresDb and ChatLogger in appnew.py
- Use existing LogModel schema (no schema changes)
- Logging calls prepared but stubbed until LLM integration
- Depends on: v1.0.2 (authentication for user metadata)
- Complexity: Low | Effort: 2-3 hours

---

## v1.0.4

**Status**: Planned
**Release Date**: TBD

### Features

- LLMAPI initialization with Azure OpenAI or Ollama
- Mode-based system prompt selection (Tutor→learning, Answer→original)
- Replace mocked responses with real streaming LLM
- Configuration from S3 (model, temperature)

### Technical Notes

- Fix S3 variable name typo in appnew.py (s3Client vs s3_client)
- Load prompts.yaml from S3, map mode to system_prompt name
- Support both OllamaLLM and AzureOpenAILLM backends
- Use ConfigurationModel for ai_model and temperature
- Depends on: v1.0.3 (config loading)
- Complexity: High | Effort: 6-8 hours

---

## v1.0.5

**Status**: Planned
**Release Date**: TBD

### Features

- Always-on context injection (remove RAG assignment logic)
- Inject assignment content into system prompt when context selected
- Personalized greeting with user name and context
- Enhanced context injection logic

### Technical Notes

- Context content from file_cache.load_cached_document()
- Prepend assignment to system prompt (not separate message)
- Greeting includes user name from AuthModel
- Everyone gets context when selected (no hash-based assignment)
- set_context() already handles session reset
- Depends on: v1.0.4 (LLM), v1.0.2 (user auth)
- Complexity: Medium | Effort: 4-5 hours

---

## v1.0.6

**Status**: Planned
**Release Date**: TBD

### Features

- Log all user prompts to database
- Log all assistant responses to database
- Include mode, context, sessionid, model, RAG flag in logs

### Technical Notes

- chat_logger.log_user_prompt() after user input
- chat_logger.log_assistant_response() after LLM response
- RAG flag always True (context always on in v2.0)
- Mode and context from session state
- Depends on: v1.0.3 (ChatLogger), v1.0.4 (LLM), v1.0.5 (context)
- Complexity: Low | Effort: 2-3 hours

---

## v1.0.7

**Status**: Planned
**Release Date**: TBD

### Features

- Admin menu in sidebar (admin users only)
- Settings page integration
- Prompts page integration
- Session debug page integration

### Technical Notes

- Add admin menu expander in sidebar after line 67 of appnew.py
- Page routing: Chat, Settings, Prompts, Session
- Conditional display based on validated=="admin"
- Reuse existing settings.py, prompts.py, session.py (no modifications)
- Depends on: v1.0.2 (admin user detection)
- Complexity: Medium | Effort: 3-4 hours

---

## v1.0.8

**Status**: Planned
**Release Date**: TBD

### Features

- About/help text for new UI
- Error handling improvements
- Loading states polish
- UI consistency checks
- Feature parity validation with app.py

### Technical Notes

- Minor UX improvements
- Add helpful error messages
- Improve loading spinners
- Optional: download chat history feature
- Depends on: All previous versions (v1.0.2-v1.0.7)
- Complexity: Low | Effort: 2-3 hours

---

## v2.0.0

**Status**: Planned
**Release Date**: TBD

### Features

- Replace app.py with appnew.py as main application
- New chat UI with mode selection (Tutor/Answer)
- Context always injected (no RAG assignment)
- Mode/context changes create new session
- Initial greeting indicating mode and context
- Full feature parity with v1.x

### Technical Notes

- **Breaking change:** Major version bump
- Backup old app.py before replacing
- appnew.py becomes the main application
- Update CLAUDE.md documentation
- Update docker-compose.yaml entry point
- New mode/context paradigm is standard
- Depends on: All previous versions complete
- Complexity: Low | Effort: 2-3 hours
- **Total v2.0 Epic Effort: 25-35 hours**

### Migration Path

v1.0.2 → Auth & Authorization
v1.0.3 → Database & Logging
v1.0.4 → LLM Integration
v1.0.5 → Context Injection
v1.0.6 → Chat Logging
v1.0.7 → Admin Pages
v1.0.8 → Polish
v2.0.0 → Release
