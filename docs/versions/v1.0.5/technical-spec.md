# Technical Specification: Context Injection Enhancement - v1.0.5

## Overview

This version implements always-on context injection for the IST256 Chatapp. When users select an assignment context (instead of "General Python"), the system will automatically inject the assignment content into the system prompt. This eliminates the experimental RAG assignment logic and ensures all users receive context-aware assistance. Additionally, the greeting message will be personalized with the user's first name and current context.

**Key Changes:**
- Remove hash-based RAG assignment logic (everyone gets context)
- Inject assignment markdown directly into system prompt when context selected
- Personalized greeting with user name from AuthModel
- Enhanced context injection using existing FileCacheDocLoader

## Architecture Changes

### Components Affected

- [/workspaces/ist256-chatapp/app/chat/appnew.py](/workspaces/ist256-chatapp/app/chat/appnew.py)
  - `get_context_injection()` function (lines 52-58) - enhance to prepend to system prompt
  - Greeting generation logic (lines 232-242) - add user name personalization
  - System prompt initialization in LLM setup (lines 177-219) - integrate context injection

- [/workspaces/ist256-chatapp/app/chat/constants.py](/workspaces/ist256-chatapp/app/chat/constants.py)
  - VERSION constant (line 1) - update to "1.0.5"
  - CONTEXT_PROMPT_TEMPLATE (lines 40-47) - may need refinement for system prompt injection

### New Components

None. This version builds on existing infrastructure.

### Dependencies

**Internal:**
- `FileCacheDocLoader` (from `app/chat/docloader.py`) - already in use for loading assignment content
- `AuthModel` (from `app/dal/models.py`) - already available in session state for user name
- `LLMAPI` (from `app/chat/llmapi.py`) - system prompt management

**External:**
No new external dependencies required.

**Version Dependencies:**
- v1.0.4 (LLM integration with LLMAPI) - MUST be complete
- v1.0.2 (Authentication with AuthModel) - MUST be complete

## Data Models

### Database Changes

No database schema changes required. The existing `LogModel` already has a `rag` boolean field which will now always be `True` when context is selected.

### API Changes

**Function Signature Modifications:**

**Current:**
```python
def get_context_injection(context: str) -> str:
    """Returns the context injection prompt based on the selected context."""
    if context != "General Python":
        content = st.session_state.file_cache.load_cached_document(context)
        return const.CONTEXT_PROMPT_TEMPLATE.format(assignment=context, content=content)
    else:
        return ""
```

**New:**
```python
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
        content = st.session_state.file_cache.load_cached_document(context)
        context_injection = const.CONTEXT_PROMPT_TEMPLATE.format(
            assignment=context,
            content=content
        )
        return context_injection + "\n\n" + system_prompt
    else:
        return system_prompt
```

## Technical Design

### Backend Implementation

#### 1. Context Injection Strategy

**Current Behavior (v1.0.4):**
- System prompt set based on mode (Tutor → "learning", Answer → "original")
- Context injection not yet implemented

**New Behavior (v1.0.5):**
- Base system prompt selected based on mode
- If context != "General Python", prepend assignment content to system prompt
- Assignment content loaded via `file_cache.load_cached_document(context)`
- Complete system prompt = `CONTEXT_PROMPT_TEMPLATE.format(assignment, content) + "\n\n" + base_system_prompt`

**Rationale:**
Prepending context to the system prompt ensures the LLM has full assignment context before processing user queries. This approach is simpler and more reliable than vector search (RAG) while providing equivalent functionality for course assignments.

#### 2. System Prompt Construction Flow

```
User selects context → set_context(mode, context) called
    ↓
Calculate context_injection string
    ↓
If context != "General Python":
    Load assignment markdown from file cache
    Format using CONTEXT_PROMPT_TEMPLATE
    Prepend to base system prompt
Else:
    Use base system prompt as-is
    ↓
Update ai.system_prompt in session state
    ↓
Clear conversation history (already done by set_context)
```

#### 3. Greeting Personalization

**Data Source:**
`st.session_state.auth_model.firstname` (from AuthModel created in v1.0.2)

**Current Greeting (lines 236-239):**
```python
if st.session_state.mode == "Tutor":
    greeting = f"I am in Tutor mode. I will provide guided learning for your {st.session_state.context} questions\n"
else:
    greeting = f"I am in Answer mode. I will provide direct answers to your {st.session_state.context} questions\n"
```

**New Greeting:**
```python
firstname = st.session_state.auth_model.firstname
if st.session_state.mode == "Tutor":
    greeting = f"Hello {firstname}! I am in Tutor mode. I will provide guided learning for your {st.session_state.context} questions.\n"
else:
    greeting = f"Hello {firstname}! I am in Answer mode. I will provide direct answers to your {st.session_state.context} questions.\n"
```

### Frontend Implementation

No UI/UX changes required. All changes are backend logic.

**User-Visible Changes:**
1. Greeting messages now include user's first name
2. LLM responses when context is selected will be more assignment-aware (due to context injection)

### Integration Points

#### MinIO S3 Integration
- **Unchanged**: Prompts loaded from S3 via `prompts.yaml` (already in v1.0.4)
- **Usage**: Base system prompts ("learning", "original") retrieved from S3

#### FileCacheDocLoader Integration
- **Location**: `/workspaces/ist256-chatapp/app/chat/docloader.py`
- **Method**: `load_cached_document(context)` - returns markdown string
- **Initialization**: Already in session state (line 132 of appnew.py)
- **Files**: Assignment markdown files in `LOCAL_FILE_CACHE` directory (env var)

#### LLM API Integration
- **LLMAPI class**: Manages system_prompt via `ai.system_prompt` attribute
- **Update Strategy**: Modify `ai.system_prompt` in `set_context()` function
- **Timing**: System prompt updated when context changes, before conversation begins

#### Authentication Integration
- **AuthModel**: Already in session state as `st.session_state.auth_model`
- **Field Used**: `auth_model.firstname` for greeting personalization
- **Source**: Extracted from Azure AD MSAL token claims (v1.0.2)

## Configuration

### Environment Variables

**No new environment variables required.**

**Existing variables used:**
- `LOCAL_FILE_CACHE` - Path to assignment markdown files (already required)
- `S3_BUCKET`, `PROMPTS_FILE` - For loading base system prompts (already required)

### Config Files

**No changes to config.yaml required.**

**constants.py updates:**
- `VERSION = "1.0.5"` (line 1)

**CONTEXT_PROMPT_TEMPLATE review:**
Current template (lines 40-47):
```python
CONTEXT_PROMPT_TEMPLATE='''
I would like to ask you questions about the assignment: {assignment}.
Please acknowledge that you are ready to answer questions about this assignment.

Here is the content of that assignment:

{content}
'''
```

**Recommended refinement for system prompt injection:**
```python
CONTEXT_PROMPT_TEMPLATE='''
You are assisting with the assignment: {assignment}

Here is the full assignment content:

{content}

---

'''
```

**Rationale:** When prepended to system prompt, we don't need the "acknowledge" request since this is injected as context, not a user message.

## Security Considerations

### Authentication Requirements
- **No changes**: User must be authenticated via Azure AD (v1.0.2)
- **Access Control**: All authenticated users (admin, exception, roster) can use context injection

### Authorization/Access Control
- **No special permissions required**: Context injection available to all user types
- **Assignment Access**: All assignments in file cache are accessible to all authenticated users

### Data Privacy Concerns
- **User Name in Greeting**: Firstname from Azure AD token already trusted
- **Assignment Content**: Course assignments are not sensitive data
- **No PII in Logs**: Assignment context logged but contains no user-specific data

### Input Validation
- **Context Selection**: Limited to dropdown values from `file_cache.get_doc_list()` + "General Python"
- **File Path Sanitization**: `FileCacheDocLoader.load_cached_document()` already validates file existence
- **No User Input**: Context content is pre-loaded from trusted file cache, not user-provided

### SQL Injection Prevention
- **Not Applicable**: No database writes in this feature
- **Future Logging**: v1.0.6 will log context to database using parameterized queries (ChatLogger)

### XSS Prevention
- **No User HTML**: Assignment content is markdown rendered by Streamlit (auto-escaped)
- **Greeting Text**: User firstname displayed via `st.write_stream()` (safe)

## Performance Considerations

### Scalability Implications
- **System Prompt Size**: Assignment markdown files range from 5-20KB
- **Concatenation Overhead**: Negligible (string concatenation in Python)
- **LLM Token Usage**: Increased context window usage (~2000-5000 tokens per assignment)
  - Impact: Slower responses, higher API costs when context selected
  - Mitigation: Acceptable tradeoff for improved answer quality

### Caching Strategies
- **File Cache**: Assignment markdown already cached in memory by FileCacheDocLoader
- **Session State**: `context_injection` stored in session state to avoid re-reading files
- **No Additional Caching**: System prompt reconstructed on context change (infrequent operation)

### Database Query Optimization
- **Not Applicable**: No database reads/writes in this feature

### API Rate Limiting
- **No Impact**: Context injection happens client-side before LLM call
- **Consideration**: Larger prompts may approach token limits for long assignments
  - Current assignments: Well within GPT-4 128K context window

### Memory Usage
- **Session State Growth**: Each session stores one `context_injection` string (~5-20KB)
- **Impact**: Minimal (24 assignments × 20KB = 480KB worst case)
- **Cleanup**: Cleared when context changes or session resets

## Error Handling

### Expected Errors and Handling Strategies

**1. File Not Found Error**
- **Scenario**: User selects context but assignment markdown missing from file cache
- **Current Behavior**: `FileCacheDocLoader.load_cached_document()` raises `FileNotFoundError`
- **Handling**: Wrap in try/except in `get_context_injection()`

```python
def get_context_injection(context: str, system_prompt: str) -> str:
    if context != "General Python":
        try:
            content = st.session_state.file_cache.load_cached_document(context)
            context_injection = const.CONTEXT_PROMPT_TEMPLATE.format(
                assignment=context,
                content=content
            )
            return context_injection + "\n\n" + system_prompt
        except FileNotFoundError:
            logger.error(f"Assignment file not found: {context}")
            st.warning(f"Assignment content for '{context}' is not available. Using general mode.")
            return system_prompt
        except Exception as e:
            logger.error(f"Error loading assignment {context}: {e}")
            return system_prompt
    else:
        return system_prompt
```

**2. YAML Template Format Error**
- **Scenario**: CONTEXT_PROMPT_TEMPLATE has invalid placeholders
- **Handling**: Will raise `KeyError` - add validation

**3. Missing AuthModel Firstname**
- **Scenario**: MSAL token missing name claim (edge case)
- **Handling**: Fallback to generic greeting

```python
firstname = st.session_state.auth_model.firstname if hasattr(st.session_state.auth_model, 'firstname') and st.session_state.auth_model.firstname else "Student"
```

### User-Facing Error Messages

- **Assignment Not Available**: "Assignment content for '{context}' is not available. Using general mode."
- **Generic Error**: "Unable to load assignment context. Please try again or select 'General Python'."

### Logging Requirements

**Log Events:**
1. Context injection success: `logger.info(f"Context injected: {context}, size: {len(content)} chars")`
2. File not found: `logger.error(f"Assignment file not found: {context}")`
3. Generic errors: `logger.error(f"Error loading assignment {context}: {e}")`

**Log Location**: Application logs via loguru (already configured in appnew.py)

### Recovery Procedures

**If Error Occurs:**
1. Log error with context name
2. Display user-friendly warning in Streamlit
3. Fallback to base system prompt (no context injection)
4. Allow user to continue with general mode or retry

**No Session Corruption**: Errors in context injection do not break the session

## Testing Strategy

### Unit Tests

**Note**: No test framework currently exists. Manual testing required.

**Future Unit Tests** (if pytest implemented):
```python
def test_get_context_injection_with_assignment():
    """Test context injection with valid assignment"""
    # Mock file_cache.load_cached_document()
    # Assert system prompt contains assignment content

def test_get_context_injection_general_python():
    """Test context injection with General Python"""
    # Assert system prompt unchanged

def test_get_context_injection_file_not_found():
    """Test graceful handling of missing assignment file"""
    # Mock FileNotFoundError
    # Assert fallback to base system prompt
```

### Integration Tests

**Manual Integration Tests:**

1. **Context Injection with Azure OpenAI**
   - Select assignment context
   - Ask question about assignment content
   - Verify LLM response shows knowledge of assignment

2. **Context Injection with Ollama**
   - Repeat above with `LLM=ollama`

3. **Mode Switching**
   - Start in Tutor mode with context
   - Switch to Answer mode
   - Verify context persists and system prompt changes

4. **Context Switching**
   - Select Lab 1
   - Ask question
   - Switch to Lab 2
   - Verify new context loaded and history cleared

### Manual Testing

**Test Scenarios:**

| Scenario | Steps | Expected Result |
|----------|-------|----------------|
| **Context Injection - Assignment** | 1. Login<br>2. Select "Intro-01-Lab"<br>3. Observe greeting | Greeting includes firstname: "Hello Mike! I am in Tutor mode..." |
| **Context Injection - General** | 1. Login<br>2. Keep "General Python"<br>3. Observe greeting | Greeting includes firstname but no assignment reference |
| **Assignment Knowledge** | 1. Select "Intro-01-Lab"<br>2. Ask "What variables are in this lab?"<br>3. Check response | LLM references specific variables from Intro-01-Lab assignment |
| **Context Switch** | 1. Start with Lab 1<br>2. Switch to Lab 2<br>3. Ask same question | LLM references Lab 2 content, not Lab 1 |
| **Mode Switch** | 1. Tutor mode with context<br>2. Switch to Answer mode<br>3. Ask question | Response style changes (Socratic → Direct), context retained |
| **Missing Assignment File** | 1. Manually delete one .md file from file cache<br>2. Select that assignment<br>3. Observe behavior | Warning displayed, fallback to general mode, no crash |
| **Admin User** | 1. Login as admin<br>2. Test context injection | Same behavior as roster user |
| **Roster User** | 1. Login as roster user<br>2. Test context injection | Full functionality available |

**Edge Cases:**
- Empty assignment file (0 bytes)
- Very large assignment (>50KB)
- Special characters in assignment content
- User with no firstname in MSAL token

## Rollback Plan

### How to Revert if Issues Arise

**Simple Rollback** (no database changes):

1. **Revert Code Changes**
   ```bash
   git revert <commit-hash-of-v1.0.5>
   git push
   ```

2. **Update VERSION Constant**
   - Edit `app/chat/constants.py`
   - Change `VERSION = "1.0.5"` back to `VERSION = "1.0.4"`

3. **Redeploy**
   - CI/CD pipeline will rebuild with reverted code
   - Monitor for successful deployment

4. **Verify Rollback**
   - Check version number in UI footer
   - Verify greeting does not include firstname
   - Verify context selection does not affect system prompt

**No Database Rollback Required**: No schema changes in this version

**No Configuration Rollback Required**: No config.yaml or prompts.yaml changes

**Impact of Rollback**: Users will lose personalized greetings and context injection, but core chat functionality remains intact

## References

- Requirements: [/workspaces/ist256-chatapp/docs/project_requirements.md](/workspaces/ist256-chatapp/docs/project_requirements.md) (lines 99-120)
- Implementation Plan: [/workspaces/ist256-chatapp/docs/versions/v1.0.5/implementation-plan.md](/workspaces/ist256-chatapp/docs/versions/v1.0.5/implementation-plan.md)
- Depends On: v1.0.4 (LLM Integration), v1.0.2 (Authentication)
- Related PRs: TBD (create PR after implementation)

---

**Generated**: 2025-12-27
**Author**: AI-assisted design via /design command
**Version**: 1.0.5
