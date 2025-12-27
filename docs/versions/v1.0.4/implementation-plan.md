# Implementation Plan: LLM Integration - v1.0.4

## Timeline

- Estimated effort: 6-8 hours
- Complexity: High
- Suggested sprint: Can be completed in 1-2 development sessions

## Phase 1: Preparation

### Tasks

- [ ] Review technical specification document
- [ ] Set up development branch: `feature/v1.0.4-llm-integration`
- [ ] Verify all LLM dependencies are available (openai, ollama packages)
- [ ] Review existing LLM backend implementations (AzureOpenAILLM, OllamaLLM)
- [ ] Review LLMAPI wrapper class for conversation management
- [ ] Test environment variables are set correctly for chosen backend
- [ ] Review prompts.yaml in S3 to understand prompt templates

### Prerequisites

- v1.0.3 completed (authentication, database, config loading)
- Azure OpenAI or Ollama endpoint configured and accessible
- S3 bucket contains valid `config.yaml` and `prompts.yaml`
- Environment variables set for chosen LLM backend

## Phase 2: Backend Implementation

### Tasks

- [ ] Fix S3 variable naming consistency in appnew.py
- [ ] Implement mode-to-prompt-name mapping dictionary
- [ ] Add LLM backend imports to appnew.py
- [ ] Implement backend selection logic (azure vs ollama)
- [ ] Initialize LLMAPI instance in session state
- [ ] Update set_context() to refresh system prompt on mode change
- [ ] Add error handling for LLM initialization failures
- [ ] Test backend initialization with both Azure and Ollama

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/appnew.py`
  - **Lines 1-20**: Add imports
    ```python
    from llm.azureopenaillm import AzureOpenAILLM
    from llm.ollamallm import OllamaLLM
    from llmapi import LLMAPI
    ```
  - **Lines 131-138**: Fix S3 client variable consistency
    - Change: Keep `s3_client` (lowercase) throughout
    - Reason: Match Python naming conventions
  - **Lines 20-33**: Update `set_context()` function
    - Add: System prompt update when mode changes
    - Change: Update AI's system prompt after clearing history
    - Reason: Ensure mode changes update teaching style
  - **Lines 148-175**: Modify config/prompts/AI initialization
    - Add: Mode-to-prompt-name mapping
    - Add: Backend selection logic
    - Add: LLMAPI initialization with system prompt
    - Change: Make system_prompt mode-aware instead of config-based
    - Reason: Enable mode switching without session refresh

### Implementation Details

**Step 1: Add Imports (after line 18)**
```python
from llm.azureopenaillm import AzureOpenAILLM
from llm.ollamallm import OllamaLLM
from llmapi import LLMAPI
```

**Step 2: Update set_context() function (lines 20-33)**

Add after `st.session_state.ai.clear_history()`:
```python
# Update system prompt based on new mode
if 'prompts' in st.session_state:
    mode_to_prompt_name = {"Tutor": "learning", "Answer": "original"}
    prompt_name = mode_to_prompt_name[mode]
    st.session_state.ai.system_prompt = st.session_state.prompts[prompt_name]
```

**Step 3: Add AI initialization (after line 163, before chat interface)**

```python
# LLM backend initialization (v1.0.4)
if 'ai' not in st.session_state:
    try:
        # Map mode to prompt name
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
```

### Files to Create

None - all required components already exist.

## Phase 3: Frontend Implementation

### Tasks

- [ ] Remove mocked response code in chat input handler
- [ ] Implement real LLM streaming response
- [ ] Add error handling for streaming failures
- [ ] Test streaming response display in UI
- [ ] Verify response is recorded in conversation history
- [ ] Test mode switching updates greeting and response style

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/appnew.py`
  - **Lines 224-238**: Replace mocked response with real LLM
    - Remove: `sleep()` and mock response
    - Add: Real LLM streaming with `ai.stream_response()`
    - Add: Error handling for streaming failures
    - Change: Record full response in AI history
    - Reason: Enable actual AI functionality

### Implementation Details

**Replace lines 233-236 with:**

```python
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

        except Exception as e:
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            st.error(error_message)
            logger.error(f"LLM streaming error: {e}")
            # Add error to chat history so user sees it on rerun
            st.session_state.messages.append({"role": "assistant", "content": error_message})
```

**Note**: Remove the existing line that adds to messages (line 238) since we're doing it inside the try/except.

## Phase 4: Configuration & Constants

### Tasks

- [ ] Update VERSION constant in constants.py to "1.0.4"
- [ ] Verify config.yaml in S3 has valid ai_model and temperature
- [ ] Verify prompts.yaml in S3 has both "learning" and "original" prompts
- [ ] Document mode-to-prompt mapping in code comments
- [ ] Verify environment variables documented in CLAUDE.md

### Configuration Changes

**File: `/workspaces/ist256-chatapp/app/chat/constants.py`**
- Line 1: Change `VERSION="1.0.3"` to `VERSION="1.0.4"`

**File: MinIO S3 `config.yaml`** (no changes required, verify exists):
```yaml
configuration:
  ai_model: gpt-4o-mini        # or another valid model
  system_prompt: learning      # Note: This field not used in v1.0.4 (mode controls it)
  temperature: 0.7
  whitelist: ist256-fall2025-roster.txt
```

**File: MinIO S3 `prompts.yaml`** (verify exists with both keys):
```yaml
prompts:
  original: "[Direct answer prompt text]"
  learning: "[Socratic teaching prompt text]"
```

**Environment Variables** (verify set correctly):
```bash
# Choose backend
LLM=azure   # or "ollama"

# If using azure:
AZURE_OPENAI_API_KEY=<key>
AZURE_OPENAI_ENDPOINT=https://ist256-openai-instance.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-08-01-preview

# If using ollama:
OLLAMA_HOST=https://ollama-proxy.cent-su.org
```

## Phase 5: Testing

### Tasks

- [ ] Manual testing checklist
  - [ ] Test Azure OpenAI backend (if available)
    - [ ] Authenticate and load app
    - [ ] Select "Tutor" mode, send message
    - [ ] Verify real AI response (not mocked)
    - [ ] Verify Socratic teaching style
    - [ ] Switch to "Answer" mode
    - [ ] Send same question
    - [ ] Verify direct answer style
  - [ ] Test Ollama backend (if available)
    - [ ] Set LLM=ollama in environment
    - [ ] Repeat Azure tests above
  - [ ] Test mode switching
    - [ ] Start in "Tutor" mode
    - [ ] Send question, get response
    - [ ] Switch to "Answer" mode
    - [ ] Verify chat history cleared
    - [ ] Verify new greeting displayed
    - [ ] Send question, verify different response style
  - [ ] Test context switching
    - [ ] Start in "General Python"
    - [ ] Send question, get response
    - [ ] Switch to "Lab 01-Intro"
    - [ ] Verify chat history cleared
    - [ ] Send question, verify response received
  - [ ] Test configuration from S3
    - [ ] Verify current temperature in config.yaml
    - [ ] Send creative question, note response
    - [ ] Modify temperature in S3 (e.g., 0.1)
    - [ ] Logout and login
    - [ ] Send same question
    - [ ] Verify less creative response
  - [ ] Test admin user access
    - [ ] Login as admin user
    - [ ] Verify LLM works same as regular user
  - [ ] Test non-admin user access
    - [ ] Login as roster user
    - [ ] Verify LLM works correctly
  - [ ] Test error scenarios
    - [ ] Invalid API key → verify error message
    - [ ] Empty prompt → verify Streamlit prevents submit
    - [ ] Very long prompt → verify response or token limit error
    - [ ] Network interruption simulation (if possible)
- [ ] Integration testing
  - [ ] Verify S3 config loading works
  - [ ] Verify prompts.yaml loading works
  - [ ] Verify mode-to-prompt mapping correct
  - [ ] Verify conversation history persists across reruns
  - [ ] Verify history cleared on mode/context change
- [ ] Performance testing
  - [ ] Test response time for typical prompt
  - [ ] Test streaming displays incrementally (not blocked)
  - [ ] Test rapid successive messages
  - [ ] Test long conversation (10+ messages)

### Test Data

**Test Prompts**:
1. "What is a variable in Python?" - Basic concept
2. "How do I read a file in Python?" - Procedural question
3. "Why am I getting a NameError?" - Debugging question
4. "Explain list comprehensions" - Advanced concept
5. "Write a function that reverses a string" - Code generation

**Expected Behaviors**:
- Tutor mode: Asks guiding questions, doesn't give direct code
- Answer mode: Provides direct answers and code examples
- Both modes: Use course terminology, avoid `if __name__ == "__main__"`, use f-strings

## Phase 6: Documentation

### Tasks

- [ ] Update CLAUDE.md with v1.0.4 changes (if needed)
- [ ] Add inline code comments for mode-to-prompt mapping
- [ ] Add docstring to set_context() if not present
- [ ] Document error handling approach in code comments
- [ ] Update docs/versions/README.md with v1.0.4 entry
- [ ] Verify technical-spec.md is accurate
- [ ] Verify implementation-plan.md is complete

### Documentation Files

**Files to Update**:
- `/workspaces/ist256-chatapp/docs/versions/README.md`
  - Add row: `| v1.0.4 | TBD | In Development | LLM Integration with mode-based prompts |`

**Files to Review** (may not need changes):
- `/workspaces/ist256-chatapp/CLAUDE.md`
  - Section "System Prompts" may need update about mode selection
  - Section "Important Files" may need reference to appnew.py changes

**Inline Code Comments to Add**:
```python
# Mode-to-prompt mapping: Tutor uses Socratic "learning" prompt,
# Answer uses direct "original" prompt
mode_to_prompt_name = {"Tutor": "learning", "Answer": "original"}
```

## Phase 7: Deployment

### Tasks

- [ ] Verify all tests passing (manual checklist complete)
- [ ] Verify no merge conflicts with main branch
- [ ] Verify VERSION updated to "1.0.4"
- [ ] Verify all documentation complete
- [ ] Commit changes with message: "Implement v1.0.4: LLM integration with mode-based prompts"
- [ ] Push feature branch to remote
- [ ] Create PR to main branch with description:
  ```
  ## Summary
  - Replace mocked responses with real LLM (Azure OpenAI or Ollama)
  - Implement mode-based system prompt selection (Tutor → learning, Answer → original)
  - Fix S3 variable naming consistency
  - Add comprehensive error handling for LLM initialization and streaming

  ## Test Plan
  - [x] Manual testing with Azure OpenAI backend
  - [x] Manual testing with Ollama backend
  - [x] Mode switching preserves functionality
  - [x] Context switching clears history
  - [x] Error scenarios display user-friendly messages

  🤖 Generated with [Claude Code](https://claude.com/claude-code)
  ```
- [ ] Request code review
- [ ] Address review feedback
- [ ] Merge to main
- [ ] Verify CI/CD pipeline passes
- [ ] Monitor deployment to staging/production
- [ ] Verify in production environment (send test message)

### Deployment Checklist

- [ ] All manual tests passing
- [ ] No merge conflicts with main
- [ ] VERSION = "1.0.4" in constants.py
- [ ] Documentation complete (technical-spec.md, implementation-plan.md, README.md)
- [ ] No breaking changes (appnew.py is separate from production app.py)
- [ ] Environment variables documented
- [ ] Error handling tested

## Dependencies

### Internal Dependencies

**Required Previous Versions**:
- v1.0.2: Authentication and authorization (MSAL, roster validation)
- v1.0.3: Database connection, ChatLogger, S3 config loading

**Blocking Issues**: None

### External Dependencies

**Third-Party Services**:
- Azure OpenAI endpoint (if using azure backend)
- Ollama proxy endpoint (if using ollama backend)
- MinIO S3 with config.yaml and prompts.yaml

**Libraries** (already in requirements.txt):
- `openai` >= 1.0.0
- `ollama` >= 0.1.0
- `loguru`
- `streamlit`
- `pyyaml`

### Team Dependencies

None - solo development project

## Risks & Mitigation

### Risk 1: LLM API Rate Limiting

- **Impact**: High (users cannot get responses)
- **Probability**: Medium (depends on usage volume)
- **Mitigation**:
  - Monitor Azure OpenAI quota usage
  - Implement user-facing error message for rate limit errors
  - Consider implementing request queuing in future version
  - Document rate limits for course instructor

### Risk 2: Streaming Response Failures

- **Impact**: Medium (degraded UX, but errors are caught)
- **Probability**: Low (stable APIs)
- **Mitigation**:
  - Comprehensive error handling with try/except
  - User-friendly error messages
  - Logging for debugging
  - Conversation history preserved even on error

### Risk 3: Prompt Injection Attacks

- **Impact**: Medium (users could manipulate AI behavior)
- **Probability**: Medium (academic environment, likely experimentation)
- **Mitigation**:
  - System prompt clearly defines AI's role
  - LLM training includes safety guardrails (Azure OpenAI content filtering)
  - Monitor chat logs for abuse (v1.0.6 will enable logging)
  - Instructor can review logged conversations

### Risk 4: Token Context Limit Exceeded

- **Impact**: Medium (long conversations fail)
- **Probability**: Medium (students may have lengthy debugging sessions)
- **Mitigation**:
  - Current: User must clear history or switch context
  - Future: Implement automatic conversation trimming
  - Document context limits in UI help text

### Risk 5: Configuration Mismatch (S3 vs Environment)

- **Impact**: Medium (wrong model or prompts loaded)
- **Probability**: Low (config managed by admin)
- **Mitigation**:
  - Validate config.yaml schema on load
  - Log configuration values at startup
  - Admin can test changes before students use app

## Success Criteria

- [ ] All tasks completed across all phases
- [ ] VERSION updated to "1.0.4" in constants.py
- [ ] Manual testing checklist complete (all items passing)
- [ ] Documentation updated (technical-spec.md, implementation-plan.md, README.md)
- [ ] Code reviewed and approved by instructor/peer
- [ ] Deployed to production environment
- [ ] No critical bugs reported within 48 hours of deployment
- [ ] Feature functions as specified in requirements:
  - [ ] Mocked responses replaced with real LLM
  - [ ] Mode selection changes teaching style (Tutor vs Answer)
  - [ ] Configuration loaded from S3 (model, temperature)
  - [ ] Streaming responses display correctly
  - [ ] Error handling prevents crashes
  - [ ] S3 variable naming consistent

## Rollback Procedure

### If Critical Issues Arise Post-Deployment

**Option 1: Full Rollback via Git Revert**
1. Identify commit hash of v1.0.4 merge: `git log --oneline`
2. Revert the commit: `git revert <commit-hash>`
3. Push to main: `git push origin main`
4. CI/CD will automatically deploy previous version
5. Verify: Send test message, should see mocked response

**Option 2: Partial Rollback (Restore Mocked Responses)**
1. Edit `/workspaces/ist256-chatapp/app/chat/appnew.py`
2. Comment out LLMAPI initialization (lines 165-190)
3. Restore mocked response code (lines 224-238):
   ```python
   with st.spinner("Thinking..."):
       sleep(random.uniform(0.5, 3.5))
       response = f"What? {prompt} !?!?"
       st.write_stream(stream_text(response))
   ```
4. Commit: `git commit -m "Hotfix: Revert to mocked responses"`
5. Push: `git push origin main`

**Option 3: Configuration Rollback (S3)**
1. Access MinIO S3 bucket
2. Restore previous version of `config.yaml`
3. Users must logout/login to reload config
4. Verify: Check logs for model/temperature values

### Verification Steps After Rollback

1. **Functional Test**:
   - Authenticate as test user
   - Send chat message
   - Verify expected behavior (mocked or previous version)

2. **Error Log Check**:
   - Review application logs: `docker logs <container-name>`
   - Check for LLM initialization errors
   - Verify no new exceptions

3. **User Communication**:
   - If rollback during class hours, notify students via announcement
   - Provide ETA for fix if applicable

## Post-Deployment

### Monitoring

**Key Metrics to Watch** (first 48 hours):
- Application error rate (Streamlit logs)
- LLM API response times (loguru logs)
- LLM API error rate (Azure portal or Ollama proxy logs)
- User session duration (indicates engagement vs frustration)
- Context switch frequency (indicates mode/context satisfaction)

**Monitoring Commands**:
```bash
# View application logs
docker logs -f ist256-chatapp

# Search for LLM errors
docker logs ist256-chatapp 2>&1 | grep -i "llm.*error"

# Check S3 config access
docker logs ist256-chatapp 2>&1 | grep -i "config.yaml"
```

**What to Monitor**:
- Startup errors (LLM initialization failures)
- Runtime errors (streaming failures)
- Performance degradation (slow response times)
- User complaints (via instructor feedback)

### Follow-up Tasks

- [ ] Collect user feedback from students (instructor survey)
- [ ] Review chat logs for prompt injection attempts (after v1.0.6)
- [ ] Monitor LLM API costs (Azure billing dashboard)
- [ ] Document common errors and resolutions
- [ ] Optimize system prompts based on user interactions
- [ ] Consider implementing conversation history trimming (future enhancement)

---

**Generated**: 2025-12-27
**Author**: AI-assisted planning via /design command
**Version**: 1.0.4
