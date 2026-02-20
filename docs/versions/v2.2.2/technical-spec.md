# Technical Specification: Mode Logging in Chat Database - v2.2.2

## Overview

Version 2.2.2 adds the `mode` field to the `LogModel` database table so that the chat mode selected by the user (Tutor or Answer) is captured in every log entry alongside the message content. Prior to this version, mode was tracked only in Streamlit session state and was lost after the session ended, making it impossible to analyze mode usage patterns or correlate LLM responses with teaching style in post-session data.

### Features Summary
- **Mode Persistence in Logs** - `mode` (Tutor/Answer) recorded in `logs` table for every user prompt and assistant response

## Architecture Changes

### Components Affected

| File | Change Type | Description |
|------|-------------|-------------|
| [/workspaces/ist256-chatapp/app/dal/models.py](../../app/dal/models.py) | Modify | Add `mode: str` field to `LogModel` (after `rag` field, line 91) |
| [/workspaces/ist256-chatapp/app/dal/chatlogger.py](../../app/dal/chatlogger.py) | Modify | Add `mode` parameter to `log()`, `log_user_prompt()`, `log_assistant_response()`; default `"system"` in `log_system_prompt()` |
| [/workspaces/ist256-chatapp/app/chat/app.py](../../app/chat/app.py) | Modify | Pass `st.session_state.mode` to both log call sites (lines ~457-462, ~483-488) |
| [/workspaces/ist256-chatapp/app/chat/constants.py](../../app/chat/constants.py) | Modify | Update VERSION to "2.2.2" (line 1) |

### New Components

None — this is a pure enhancement to existing components with no new files required.

### Dependencies

No new external dependencies. Uses existing:
- `sqlmodel` / `pydantic` for data models
- `loguru` for logging
- `streamlit` for session state access

## Data Models

### Database Changes

**`LogModel`** ([app/dal/models.py](../../app/dal/models.py)):

```python
# Before (v2.2.1):
class LogModel(SQLModel, table=True):
    __tablename__ = "logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    sessionid: str
    userid: str
    timestamp: str
    model: str
    rag: bool
    context: str
    role: str
    content: str

# After (v2.2.2):
class LogModel(SQLModel, table=True):
    __tablename__ = "logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    sessionid: str
    userid: str
    timestamp: str
    model: str
    rag: bool
    mode: str          # ← NEW FIELD
    context: str
    role: str
    content: str
```

**Migration:**
- **New installs**: `SQLModel.metadata.create_all()` automatically creates the `mode` column on first startup — no action required.
- **Existing databases**: Run the following SQL migration before deploying:
  ```sql
  ALTER TABLE logs ADD COLUMN mode VARCHAR NOT NULL DEFAULT 'Unknown';
  ```
  The default `'Unknown'` ensures existing rows remain valid.

### API Changes

**`ChatLogger`** ([app/dal/chatlogger.py](../../app/dal/chatlogger.py)):

```python
# Before (v2.2.1):
def log(self, sessionid, userid, timestamp, model, rag, context, role, content):
def log_user_prompt(self, sessionid, userid, context, prompt):
def log_assistant_response(self, sessionid, userid, context, response):
def log_system_prompt(self, appid, userid, system_prompt):

# After (v2.2.2):
def log(self, sessionid, userid, timestamp, model, rag, mode, context, role, content):
def log_user_prompt(self, sessionid, userid, mode, context, prompt):
def log_assistant_response(self, sessionid, userid, mode, context, response):
def log_system_prompt(self, appid, userid, system_prompt):  # unchanged — passes mode="system" internally
```

## Technical Design

### Backend Implementation

#### 1. `LogModel` Field Addition ([app/dal/models.py](../../app/dal/models.py))

Add `mode: str` between `rag` and `context`. No default value — callers must always supply mode to ensure the field is always populated.

#### 2. `ChatLogger` Signature Update ([app/dal/chatlogger.py](../../app/dal/chatlogger.py))

The `log()` core method is updated to accept `mode` between `rag` and `context` in its parameter list. The two public-facing convenience methods `log_user_prompt()` and `log_assistant_response()` gain a `mode` parameter inserted after `userid`. The internal `log_system_prompt()` passes `mode="system"` as a constant so its external interface is unchanged.

**Data flow through `log_user_prompt()`:**
```
app.py call site
  → log_user_prompt(sessionid, userid, mode, context, prompt)
    → log(sessionid, userid, timestamp(), model, rag, mode, context, "user", prompt)
      → LogModel(mode=mode, ...)
        → PostgreSQL logs table
```

#### 3. Call Site Update ([app/chat/app.py](../../app/chat/app.py))

Two call sites need updating to pass `st.session_state.mode`:

**User prompt log (around line 457):**
```python
# Before:
st.session_state.chat_logger.log_user_prompt(
    st.session_state.sessionid,
    st.session_state.auth_model.email,
    st.session_state.context,
    prompt
)

# After:
st.session_state.chat_logger.log_user_prompt(
    st.session_state.sessionid,
    st.session_state.auth_model.email,
    st.session_state.mode,
    st.session_state.context,
    prompt
)
```

**Assistant response log (around line 483):**
```python
# Before:
st.session_state.chat_logger.log_assistant_response(
    st.session_state.sessionid,
    st.session_state.auth_model.email,
    st.session_state.context,
    full_response
)

# After:
st.session_state.chat_logger.log_assistant_response(
    st.session_state.sessionid,
    st.session_state.auth_model.email,
    st.session_state.mode,
    st.session_state.context,
    full_response
)
```

`st.session_state.mode` is set during session initialization from user preferences (v1.0.10) and updated when the user changes mode, so it is always populated before any chat message is logged.

### Frontend Implementation

No UI changes — this is a pure backend/data-layer enhancement. Users do not see any difference; the mode is silently captured with each interaction.

### Integration Points

| Component | Integration |
|-----------|-------------|
| **PostgreSQL** | `mode` persisted to `logs` table via SQLModel |
| **Streamlit Session State** | `st.session_state.mode` read at log call sites |
| **ChatLogger** | Updated API propagates mode through all log methods |
| **MinIO S3** | No change |
| **LLM API** | No change |
| **Authentication** | No change |

## Configuration

### Environment Variables

No new or modified environment variables.

### Config Files

No changes to `config.yaml`, `prompts.yaml`, or `constants.py` beyond the VERSION bump.

**VERSION constant update** ([app/chat/constants.py](../../app/chat/constants.py)):
```python
VERSION="2.2.2"
```

## Security Considerations

| Consideration | Handling |
|---------------|----------|
| **Data exposure** | `mode` is a non-sensitive string ("Tutor" / "Answer") — no PII risk |
| **SQL injection** | SQLModel ORM parameterizes all inserts — no raw SQL used |
| **Input validation** | `mode` comes from a controlled constant (`MODES` list in constants.py), not from user-provided free text |
| **Access control** | No change — logs remain accessible only to admin users via export page |

## Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Database writes** | One additional VARCHAR column per INSERT — negligible overhead |
| **Session state** | Reading `st.session_state.mode` is O(1) — no overhead |
| **Schema migration** | One-time `ALTER TABLE` — no ongoing performance impact |
| **Index** | Adding `mode` as a future index candidate would support analytics queries (not part of this version) |

## Error Handling

| Error | Handling | User Message |
|-------|----------|--------------|
| **`mode` not in session state** | Extremely unlikely — mode is set at login. Would surface as `KeyError` in logs | Existing log error handling catches and logs the exception |
| **Database write failure** | Existing `try/except` in app.py catches and logs — user sees no error | (Silent — existing behavior) |
| **Schema migration not run** | `mode` column missing — INSERT fails with `psycopg2.errors.UndefinedColumn` | Existing error handling logs the exception; run migration before deploy |

### Logging

No new log statements required. The existing `logger.debug()` calls on log success and `logger.error()` on failure cover this feature naturally.

## Testing Strategy

### Unit Tests

| Test Case | Description |
|-----------|-------------|
| `test_log_model_has_mode_field` | `LogModel` instantiation includes `mode` field without error |
| `test_chatlogger_log_user_prompt_with_mode` | `log_user_prompt()` passes mode correctly to `log()` |
| `test_chatlogger_log_assistant_response_with_mode` | `log_assistant_response()` passes mode correctly to `log()` |
| `test_chatlogger_log_system_prompt_uses_system_mode` | `log_system_prompt()` passes `mode="system"` automatically |

### Integration Tests

| Test Case | Description |
|-----------|-------------|
| **Tutor mode chat** | Send a message in Tutor mode; query `logs` table; verify `mode = 'Tutor'` |
| **Answer mode chat** | Send a message in Answer mode; query `logs` table; verify `mode = 'Answer'` |
| **Mode switch** | Switch from Tutor to Answer mid-session; verify new messages logged with new mode |
| **Export includes mode** | Export CSV/JSON via admin export page; verify `mode` column present |

### Manual Testing Checklist

#### Database Verification
- [ ] Send a chat message in Tutor mode
- [ ] Query database: `SELECT mode, role, content FROM logs ORDER BY id DESC LIMIT 5;`
- [ ] Confirm `mode = 'Tutor'` for both user and assistant rows
- [ ] Switch to Answer mode, send another message
- [ ] Confirm new rows show `mode = 'Answer'`
- [ ] Confirm older rows still show `mode = 'Tutor'`

#### Export Verification
- [ ] Export chat logs as CSV via Admin → Export
- [ ] Open CSV and confirm `mode` column is present and populated
- [ ] Export as JSON and confirm `mode` field is present in each log object

#### Regression Testing
- [ ] App starts without errors after schema change
- [ ] Tutor mode chat still works normally
- [ ] Answer mode chat still works normally
- [ ] Context selection still works normally
- [ ] Admin pages (Settings, Whitelist, Session, Export) still load
- [ ] Session page displays correct session info

#### Edge Cases
- [ ] First message of a new session correctly logs mode
- [ ] Mode logged even when context is "General Python"
- [ ] Mode logged for both user and assistant roles
- [ ] `log_system_prompt()` still works without mode parameter

## Rollback Plan

1. **Revert code changes**
   ```bash
   git revert <v2.2.2-commit-hash>
   ```
2. **Database rollback** (if needed — only if deploy caused issues)
   ```sql
   ALTER TABLE logs DROP COLUMN mode;
   ```
   Note: Dropping the column removes all `mode` data for existing rows; only do this if the migration was fully applied and the column must be removed.
3. **Verification after rollback**
   - App starts and accepts chat messages without errors
   - `SELECT * FROM logs LIMIT 1;` shows no `mode` column
   - Export works without `mode` field

## References

- Requirements: [/workspaces/ist256-chatapp/docs/project_requirements.md](../../docs/project_requirements.md) (v2.2.2 section)
- LogModel: [/workspaces/ist256-chatapp/app/dal/models.py](../../app/dal/models.py) (lines 84-94)
- ChatLogger: [/workspaces/ist256-chatapp/app/dal/chatlogger.py](../../app/dal/chatlogger.py)
- Main app log call sites: [/workspaces/ist256-chatapp/app/chat/app.py](../../app/chat/app.py) (lines ~457, ~483)
- Mode constants: [/workspaces/ist256-chatapp/app/chat/constants.py](../../app/chat/constants.py) (`MODES = ["Tutor", "Answer"]`)
- Previous version (v2.2.1): [/workspaces/ist256-chatapp/docs/versions/v2.2.1/](../v2.2.1/)

---

**Generated**: 2026-02-20
**Author**: AI-assisted design via /design command
**Version**: 2.2.2
