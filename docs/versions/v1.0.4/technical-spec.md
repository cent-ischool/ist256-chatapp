# Technical Specification: LLM Integration - v1.0.4

## Overview

This version integrates real LLM functionality into appnew.py, replacing the mocked "What? !?!?" responses with actual AI responses from Azure OpenAI or Ollama. The implementation includes:

- LLMAPI initialization with backend selection (Azure OpenAI or Ollama)
- Mode-based system prompt selection (Tutor → "learning", Answer → "original")
- Configuration loading from S3 (ai_model, temperature, system_prompt)
- Streaming LLM responses to the chat interface
- Fix for S3 variable naming inconsistency (s3Client vs s3_client)

This version completes the core LLM integration layer, preparing the foundation for context injection (v1.0.5) and chat logging (v1.0.6).

## Architecture Changes

### Components Affected

- `/workspaces/ist256-chatapp/app/chat/appnew.py`
  - Lines 1-20: Add LLMAPI import and backend imports
  - Lines 131-138: Fix S3 client variable name from `s3_client` to `s3Client` for consistency
  - Lines 148-164: Modify config/prompts loading to support mode-based prompt selection
  - Lines 164-175: Add LLMAPI initialization with backend strategy pattern
  - Lines 224-238: Replace mocked response with real LLM streaming

- `/workspaces/ist256-chatapp/app/chat/constants.py`
  - Line 1: Update VERSION from "1.0.3" to "1.0.4"

### New Components

None - this version uses existing backend implementations (AzureOpenAILLM, OllamaLLM, LLMAPI).

### Dependencies

**Python Libraries** (already in requirements.txt):
- `openai` - Azure OpenAI client
- `ollama` - Ollama client
- `loguru` - Logging

**Internal Modules**:
- `app.llm.azureopenaillm.AzureOpenAILLM` - Azure backend
- `app.llm.ollamallm.OllamaLLM` - Ollama backend
- `app.chat.llmapi.LLMAPI` - Conversation wrapper

**Environment Variables**:
- `LLM` - Backend selection ("azure" or "ollama")
- `AZURE_OPENAI_API_KEY` - Azure API key (if using azure)
- `AZURE_OPENAI_ENDPOINT` - Azure endpoint URL (if using azure)
- `AZURE_OPENAI_API_VERSION` - Azure API version (if using azure)
- `OLLAMA_HOST` - Ollama host URL (if using ollama)

## Data Models

### Database Changes

None - LogModel schema remains unchanged. Chat logging will be implemented in v1.0.6.

### API Changes

None - this version uses existing LLMAPI interface:
- `LLMAPI.stream_response(user_query: str, ignore_history: bool) -> Generator[str]`
- `LLMAPI.record_response(assistant_response: str) -> None`
- `LLMAPI.clear_history() -> None`

## Technical Design

### Backend Implementation

**1. S3 Variable Name Fix**

Current code has inconsistency:
- Line 132: `s3_client = S3Client(...)`
- Line 138: `st.session_state.s3_client = s3_client`
- Line 149: `st.session_state.s3_client.get_text_file(...)` (correct)

However, other parts of the codebase use `s3Client` (uppercase C). Standardize to `s3_client` (lowercase) throughout appnew.py to match Python naming conventions.

**2. Mode-to-Prompt Mapping**

The configuration loading section (lines 148-154) currently loads:
- `config.system_prompt` - contains "learning" or "original"
- `prompts[config.system_prompt]` - the actual prompt text

For v1.0.4, we need to map the mode selection to the prompt:
- Mode "Tutor" → system_prompt = "learning"
- Mode "Answer" → system_prompt = "original"

Implementation approach:
```python
# Map mode to system_prompt name
mode_to_prompt_name = {
    "Tutor": "learning",
    "Answer": "original"
}

# Get the prompt name based on current mode
prompt_name = mode_to_prompt_name[st.session_state.mode]

# Get the actual prompt text
system_prompt = prompts[prompt_name]
```

This allows users to switch modes and get the appropriate teaching style.

**3. LLM Backend Selection**

Use environment variable `LLM` to choose backend:

```python
import os
from llm.azureopenaillm import AzureOpenAILLM
from llm.ollamallm import OllamaLLM
from llmapi import LLMAPI

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
```

**4. LLMAPI Initialization**

Create LLMAPI instance with the backend and system prompt:

```python
ai = LLMAPI(
    llm=backend,
    model=st.session_state.config.ai_model,
    temperature=st.session_state.config.temperature,
    system_prompt=system_prompt
)
st.session_state.ai = ai
```

**5. Clear History on Context Change**

The `set_context()` function (lines 20-33) already clears the AI history:
```python
if 'ai' in st.session_state:
    st.session_state.ai.clear_history()
```

This ensures that when the user changes mode or context, the conversation history is reset. However, the system prompt should also be updated to match the new mode.

**Updated set_context() approach:**
```python
def set_context(mode: str, context: str):
    # ... existing code ...

    # Update system prompt if AI exists
    if 'ai' in st.session_state:
        st.session_state.ai.clear_history()
        # Update system prompt based on new mode
        mode_to_prompt_name = {"Tutor": "learning", "Answer": "original"}
        prompt_name = mode_to_prompt_name[mode]
        st.session_state.ai.system_prompt = st.session_state.prompts[prompt_name]
```

### Frontend Implementation

**Streaming Response Display**

Replace the mocked response (lines 233-236) with real LLM streaming:

```python
# Current (mocked):
with st.spinner("Thinking..."):
    sleep(random.uniform(0.5, 3.5))  # Simulate thinking time
    response = f"What? {prompt} !?!?"
    st.write_stream(stream_text(response))

# New (real LLM):
with st.spinner("Thinking..."):
    response_stream = st.session_state.ai.stream_response(prompt)
    full_response = st.write_stream(response_stream)
    st.session_state.ai.record_response(full_response)
```

Key changes:
- Remove mock delay (`sleep`)
- Call `ai.stream_response(prompt)` to get streaming generator
- Use `st.write_stream()` to display chunks (returns assembled text)
- Record full response in conversation history via `ai.record_response()`

**Note**: `st.write_stream()` in Streamlit accepts a generator and returns the fully assembled text, which we need to record in the AI's message history.

### Integration Points

**MinIO S3 Integration**:
- Load `config.yaml` for ai_model, temperature, system_prompt name
- Load `prompts.yaml` for system prompt text templates
- S3 client already initialized in session state (lines 131-138)

**PostgreSQL Integration**:
- Not used in this version
- ChatLogger already initialized (lines 156-163) but not called
- Logging deferred to v1.0.6

**LLM API Integration**:
- Backend chosen via `LLM` environment variable
- AzureOpenAI: uses api_key, endpoint, api_version
- Ollama: uses host_url
- Both support streaming via `generate_stream()`

**Authentication/Authorization**:
- No changes to auth flow
- LLM available to all authenticated users (admin, exception, roster)

**Streamlit Session State**:
- Add `st.session_state.ai` (LLMAPI instance)
- Add `st.session_state.prompts` (prompt dictionary)
- Update `st.session_state.system_prompt_text` to be mode-aware

## Configuration

### Environment Variables

**Required (no changes, already documented)**:
- `LLM` - "azure" or "ollama"
- `AZURE_OPENAI_API_KEY` - Azure API key (required if LLM=azure)
- `AZURE_OPENAI_ENDPOINT` - Azure endpoint (required if LLM=azure)
- `AZURE_OPENAI_API_VERSION` - Azure API version (required if LLM=azure)
- `OLLAMA_HOST` - Ollama host URL (required if LLM=ollama)

### Config Files

**config.yaml** (stored in MinIO S3):
```yaml
configuration:
  ai_model: gpt-4o-mini        # Model name (Azure deployment or Ollama model)
  system_prompt: learning      # "learning" or "original"
  temperature: 0.7             # 0.0-1.0
  whitelist: roster.txt
```

**prompts.yaml** (stored in MinIO S3):
```yaml
prompts:
  original: "Direct answer mode prompt..."
  learning: "Socratic teaching mode prompt..."
```

**Notes**:
- Mode selection in UI ("Tutor" or "Answer") maps to prompt name ("learning" or "original")
- Config loading happens once per session (lines 148-154)
- Changes to config require session refresh or logout/login

## Security Considerations

**Authentication Requirements**:
- LLM functionality requires authenticated user (Azure AD MSAL)
- No additional authentication needed for LLM APIs (handled via env vars)

**Authorization/Access Control**:
- All user types (admin, exception, roster) can access LLM
- No privilege escalation risks

**Data Privacy**:
- User prompts sent to external LLM (Azure OpenAI or Ollama proxy)
- No PII sent to LLM (user email not included in prompts)
- Conversation history stored in session state (memory only, cleared on logout)

**Input Validation**:
- Streamlit handles basic XSS prevention for chat input
- No SQL queries in this version (logging in v1.0.6)
- LLM responses rendered as Markdown (Streamlit sanitizes)

**SQL Injection Prevention**:
- Not applicable (no database writes in this version)

**XSS Prevention**:
- Streamlit's `st.markdown()` sanitizes HTML by default
- User input passed to LLM, not directly rendered as HTML

**API Key Security**:
- API keys stored in environment variables (not in code)
- Not exposed to frontend or logs
- loguru logging in LLM backends logs endpoint/model but not keys

## Performance Considerations

**Scalability Implications**:
- Each user session creates one LLMAPI instance (stored in session state)
- LLM API rate limits apply (Azure OpenAI TPM/RPM limits)
- Streaming reduces perceived latency vs. blocking calls

**Caching Strategies**:
- Config and prompts loaded once per session (lines 148-154)
- No caching of LLM responses (each query hits API)
- Session state persists AI instance across reruns (avoids reinit)

**Database Query Optimization**:
- Not applicable (no database reads/writes in this version)

**API Rate Limiting**:
- Dependent on Azure OpenAI deployment quotas
- Ollama proxy may have rate limits
- No client-side rate limiting implemented

**Memory Usage**:
- Conversation history grows with each message (stored in LLMAPI._messages)
- No automatic trimming of old messages
- Long conversations may hit token context limits (model-dependent)

**Recommendation**: Future versions could add conversation history trimming to prevent token limit errors.

## Error Handling

### Expected Errors and Handling Strategies

**1. LLM Backend Initialization Failure**

Scenario: Invalid API key, unreachable endpoint, missing environment variable

Handling:
```python
try:
    if os.environ["LLM"] == "azure":
        backend = AzureOpenAILLM(...)
    else:
        backend = OllamaLLM(...)
except KeyError as e:
    st.error(f"Configuration error: Missing environment variable {e}")
    st.stop()
except Exception as e:
    st.error(f"Failed to initialize LLM backend: {e}")
    st.stop()
```

**2. Streaming Response Failure**

Scenario: API timeout, rate limit exceeded, network error during streaming

Handling:
```python
try:
    response_stream = st.session_state.ai.stream_response(prompt)
    full_response = st.write_stream(response_stream)
    st.session_state.ai.record_response(full_response)
except Exception as e:
    st.error(f"Failed to get response from AI: {e}")
    logger.error(f"LLM streaming error: {e}")
    # Don't add failed message to history
```

**3. Config/Prompts Loading Failure**

Scenario: S3 file not found, YAML parse error

Handling: Already handled in lines 148-154 (would raise exception, caught by Streamlit)

### User-Facing Error Messages

- "Configuration error: Missing environment variable LLM" - Missing required env var
- "Failed to initialize LLM backend: [details]" - Backend initialization failed
- "Failed to get response from AI: [details]" - Streaming error during chat

### Logging Requirements

- Use loguru logger for backend errors (already implemented in LLM classes)
- Log LLM initialization parameters (endpoint, model, temperature)
- Log streaming errors with full exception details
- Do NOT log user prompts or API keys

### Recovery Procedures

- Backend init failure: User must fix environment variables and refresh
- Streaming failure: User can retry prompt (history preserved)
- Config load failure: Admin must fix S3 config files

## Testing Strategy

### Unit Tests

Not applicable - no test suite exists yet (pytest installed but no tests written).

Future unit test cases would include:
- `test_mode_to_prompt_mapping()` - verify "Tutor" → "learning", "Answer" → "original"
- `test_backend_selection_azure()` - verify AzureOpenAILLM initialized when LLM=azure
- `test_backend_selection_ollama()` - verify OllamaLLM initialized when LLM=ollama
- `test_system_prompt_update_on_mode_change()` - verify set_context updates prompt

### Integration Tests

Manual integration testing required (no automated tests):

**Test Case 1: Azure OpenAI Backend**
1. Set `LLM=azure` in environment
2. Set valid Azure credentials
3. Start app, authenticate
4. Send chat message in "Tutor" mode
5. Verify: Real AI response (not mocked), Socratic teaching style
6. Switch to "Answer" mode
7. Send same question
8. Verify: Real AI response, direct answer style

**Test Case 2: Ollama Backend**
1. Set `LLM=ollama` in environment
2. Set valid `OLLAMA_HOST`
3. Repeat Test Case 1 steps

**Test Case 3: Mode Switching**
1. Start in "Tutor" mode, send message, get response
2. Switch to "Answer" mode (triggers set_context)
3. Verify: Chat history cleared, new greeting displayed
4. Send message
5. Verify: Response uses "original" prompt style

**Test Case 4: Context Switching**
1. Start in "General Python" context
2. Send message, get response
3. Switch to "Lab 01-Intro" context
4. Verify: Chat history cleared, new greeting displayed
5. Send message
6. Verify: Response received (context injection in v1.0.5)

**Test Case 5: Configuration from S3**
1. Modify config.yaml in S3 (change temperature to 0.1)
2. Logout and login (refresh session)
3. Send message
4. Verify: Response uses new temperature (less creative)

### Manual Testing

**Admin vs Non-Admin Testing**:
- Not applicable (LLM available to all user types)

**Edge Cases to Verify**:
1. Very long user prompt (test token limits)
2. Empty prompt (should Streamlit prevent this?)
3. Rapid successive messages (test streaming concurrency)
4. Special characters in prompt (test encoding)
5. Mode switch during active stream (unlikely but test behavior)

**Browser Testing**:
- Test in Chrome, Firefox, Safari
- Verify streaming displays correctly across browsers

**Error Scenario Testing**:
1. Invalid API key → error message displayed
2. Unreachable endpoint → timeout error displayed
3. Rate limit exceeded → error message displayed
4. Network interruption during stream → partial response handling

## Rollback Plan

**How to Revert if Issues Arise**:

1. **Immediate Rollback** (critical production issue):
   ```bash
   git revert <commit-hash>
   git push origin main
   ```
   CI/CD pipeline will deploy previous version.

2. **Partial Rollback** (revert to mocked responses):
   - Edit `/workspaces/ist256-chatapp/app/chat/appnew.py` lines 224-238
   - Restore mocked response code:
     ```python
     with st.spinner("Thinking..."):
         sleep(random.uniform(0.5, 3.5))
         response = f"What? {prompt} !?!?"
         st.write_stream(stream_text(response))
     ```
   - Comment out LLMAPI initialization
   - Commit and push

3. **Configuration Rollback** (bad config in S3):
   - Restore previous `config.yaml` version in MinIO S3
   - Users must logout/login to reload config

4. **Environment Variable Rollback**:
   - Check `.env` file or Kubernetes secrets
   - Restore previous LLM backend settings
   - Restart application

**Verification After Rollback**:
- Send test message in chat interface
- Verify either: mocked response (partial rollback) or previous version behavior (full rollback)
- Check logs for errors

## References

- Related issues: N/A
- Related PRs: N/A
- External docs:
  - [Azure OpenAI Python SDK](https://github.com/openai/openai-python)
  - [Ollama Python SDK](https://github.com/ollama/ollama-python)
  - [Streamlit Streaming](https://docs.streamlit.io/develop/api-reference/write-magic/st.write_stream)

---

**Generated**: 2025-12-27
**Author**: AI-assisted design via /design command
**Version**: 1.0.4
