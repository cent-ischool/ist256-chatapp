# Technical Specification: Chat Logging - v1.0.6

## Overview

Version 1.0.6 adds comprehensive chat logging functionality to the IST256 Chatapp. This feature logs all user prompts and assistant responses to the PostgreSQL database, enabling tracking of student interactions, usage analytics, and audit trails. The logging captures essential metadata including mode (Tutor/Answer), context (assignment or General Python), session ID, model used, and RAG flag (always true in v2.0).

This is a low-complexity feature that leverages the existing ChatLogger infrastructure already initialized in v1.0.3.

## Architecture Changes

### Components Affected

- `/workspaces/ist256-chatapp/app/chat/appnew.py` (lines 310-336)
  - Add logging calls after user input and LLM response
  - No structural changes, only two additional function calls

### New Components

None. All required components already exist:
- ChatLogger class already exists in `/workspaces/ist256-chatapp/app/chatlogger.py`
- LogModel already exists in `/workspaces/ist256-chatapp/app/dal/models.py`
- Database connection already initialized in appnew.py (v1.0.3)

### Dependencies

**Internal Dependencies:**
- v1.0.2: User authentication (provides userid/email)
- v1.0.3: ChatLogger and database initialization
- v1.0.4: LLM integration (provides model metadata)
- v1.0.5: Context injection (provides context metadata)

**External Libraries:**
All required libraries already installed:
- `sqlmodel`: Database ORM
- `loguru`: Application logging (for debugging)

## Data Models

### Database Changes

**No schema changes required.** The existing `LogModel` table (created in v1.0.3) already supports all required fields:

```python
class LogModel(SQLModel, table=True):
    __tablename__ = "logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    sessionid: str          # UUID4 session identifier
    userid: str             # User email from auth
    timestamp: str          # ISO 8601 timestamp
    model: str              # AI model name (e.g., "gpt-4o")
    rag: bool               # True in v2.0 (context always available)
    context: str            # Assignment name or "General Python"
    role: str               # "user" or "assistant"
    content: str            # Message text
```

### API Changes

No API changes. Uses existing ChatLogger methods:

```python
chat_logger.log_user_prompt(sessionid, userid, context, prompt)
chat_logger.log_assistant_response(sessionid, userid, context, response)
```

## Technical Design

### Backend Implementation

**Location:** `/workspaces/ist256-chatapp/app/chat/appnew.py`

**Implementation Steps:**

1. **User Prompt Logging (after line 315)**
   - After user message is added to `st.session_state.messages`
   - Call `st.session_state.chat_logger.log_user_prompt()`
   - Pass: `sessionid`, `userid` (email), `context`, `prompt`
   - ChatLogger internally adds: `timestamp`, `model`, `rag=True`, `role="user"`

2. **Assistant Response Logging (after line 329)**
   - After assistant response is added to `st.session_state.messages`
   - Call `st.session_state.chat_logger.log_assistant_response()`
   - Pass: `sessionid`, `userid` (email), `context`, `full_response`
   - ChatLogger internally adds: `timestamp`, `model`, `rag=True`, `role="assistant"`

**Error Handling:**
- Wrap logging calls in try/except to prevent chat failures if DB unavailable
- Log errors to loguru logger for debugging
- Continue normal chat flow even if logging fails (graceful degradation)

**Code Pattern (existing pattern from app.py lines 246-247, 263-264):**

```python
# After user message
st.session_state.messages.append({"role": "user", "content": prompt})
# ADD: Log user prompt
try:
    st.session_state.chat_logger.log_user_prompt(
        st.session_state.sessionid,
        st.session_state.auth_model.email,
        st.session_state.context,
        prompt
    )
except Exception as e:
    logger.error(f"Failed to log user prompt: {e}")

# After assistant response
st.session_state.messages.append({"role": "assistant", "content": full_response})
# ADD: Log assistant response
try:
    st.session_state.chat_logger.log_assistant_response(
        st.session_state.sessionid,
        st.session_state.auth_model.email,
        st.session_state.context,
        full_response
    )
except Exception as e:
    logger.error(f"Failed to log assistant response: {e}")
```

### Frontend Implementation

No UI changes. Logging is transparent to the user.

### Integration Points

**PostgreSQL Integration:**
- ChatLogger uses `st.session_state.db` (PostgresDb instance)
- Calls `session.add(LogModel(...))` and `session.commit()`
- Connection pooling handled by SQLModel/SQLAlchemy
- Transactions are auto-committed (single insert per log call)

**Session State Integration:**
- `st.session_state.chat_logger`: ChatLogger instance (initialized in v1.0.3)
- `st.session_state.sessionid`: UUID4 session ID (set by set_context())
- `st.session_state.auth_model.email`: User email (from v1.0.2 auth)
- `st.session_state.context`: Current assignment or "General Python" (from v1.0.5)
- `st.session_state.config.ai_model`: Model name (from v1.0.4)

**ChatLogger Integration:**
- ChatLogger initialized at line 196-202 in appnew.py
- Constructor params: `db`, `model`, `rag=True`
- Model and RAG flag stored in ChatLogger instance
- Logging methods auto-populate timestamp, model, rag, role fields

## Configuration

### Environment Variables

No new environment variables required. Uses existing:
- `DATABASE_URL`: PostgreSQL connection string (required since v1.0.3)

### Config Files

No changes to config files:
- `config.yaml`: No changes
- `prompts.yaml`: No changes
- `constants.py`: VERSION updated to "1.0.6" (see Phase 4)

## Security Considerations

**Data Privacy:**
- All chat messages (user and assistant) stored in database
- Contains student prompts (may include code, assignment answers)
- Database access restricted to application service account
- No personally identifiable information beyond email address
- Email already required for authentication

**Access Control:**
- Only database service account can write logs
- Admin users may need read access for analytics (future feature)
- No user-facing interface to view logs in this version

**SQL Injection Prevention:**
- SQLModel ORM handles parameterization automatically
- No raw SQL queries used
- LogModel fields are strongly typed

**Input Validation:**
- `sessionid`: UUID4 format (validated by Python uuid module)
- `userid`: Email format (validated by MSAL authentication)
- `context`: Limited to assignment list + "General Python" (UI dropdown)
- `prompt` and `response`: Free text (no validation needed, stored as-is)

**Audit Trail:**
- Logs create immutable audit trail of all interactions
- Timestamps are UTC ISO 8601 format
- Session IDs allow tracking conversation flows

## Performance Considerations

**Database Impact:**
- Two INSERT queries per chat exchange (user + assistant)
- Minimal impact: single-row inserts with indexed primary key
- No complex joins or subqueries
- Expected volume: ~100-500 messages/day per user in active development

**Scalability:**
- LogModel table will grow over time (~2 rows per message exchange)
- Recommended: Add index on `userid` and `timestamp` for future analytics
- Consider archiving/partitioning strategy for multi-year data (future work)

**Caching:**
- No caching needed (write-only operation)
- Each log call is independent transaction

**Response Time:**
- Logging is synchronous but very fast (<10ms per insert)
- Minimal user-perceived latency
- Error handling prevents blocking on DB failures

**Memory Usage:**
- No additional memory overhead (data immediately persisted)
- ChatLogger instance is lightweight (just holds db reference and metadata)

## Error Handling

### Expected Errors

**1. Database Connection Failure**
- **Scenario:** PostgreSQL unavailable or network issue
- **Handling:** Catch exception, log to loguru, continue chat
- **User Experience:** Chat continues normally (logging fails silently)
- **Recovery:** Logging resumes when DB reconnects

**2. Database Write Failure**
- **Scenario:** Constraint violation, disk full, permissions issue
- **Handling:** Catch exception, log detailed error to loguru
- **User Experience:** No user-facing error (chat unaffected)
- **Recovery:** Check database logs, fix underlying issue

**3. Session State Missing**
- **Scenario:** `chat_logger`, `sessionid`, or `auth_model` not in session state
- **Handling:** Should not occur (initialized earlier in flow)
- **Mitigation:** Defensive checks in logging code
- **User Experience:** Chat continues, logging skipped

### User-Facing Error Messages

None. Logging failures are transparent to users. Errors logged internally:

```python
logger.error(f"Failed to log user prompt: {e}")
logger.error(f"Failed to log assistant response: {e}")
```

### Logging Requirements

**Application Logs (loguru):**
- Log successful logging calls at DEBUG level
- Log failures at ERROR level with exception details
- Include session ID and user email in error logs for debugging

**Database Logs:**
- PostgreSQL logs handle constraint violations and connection errors
- Monitor for repeated failures indicating systemic issues

### Recovery Procedures

**If logging fails:**
1. Chat functionality unaffected (graceful degradation)
2. Check PostgreSQL connection and credentials
3. Verify LogModel table schema matches expectations
4. Review application logs for exception details
5. Test ChatLogger.log() directly for debugging

## Testing Strategy

### Unit Tests

**Currently no test framework in place.** When pytest suite is added:

1. **Test ChatLogger.log_user_prompt()**
   - Verify LogModel created with correct fields
   - Verify `role="user"` and timestamp auto-populated
   - Verify database insert succeeds

2. **Test ChatLogger.log_assistant_response()**
   - Verify LogModel created with correct fields
   - Verify `role="assistant"` and timestamp auto-populated
   - Verify database insert succeeds

3. **Test error handling**
   - Mock database failure, verify exception caught
   - Verify logging continues after transient failures

### Integration Tests

**Manual testing required:**

1. **User prompt logging**
   - Send chat message
   - Query database: `SELECT * FROM logs WHERE role='user' ORDER BY id DESC LIMIT 1`
   - Verify: sessionid, userid, context, content, timestamp, model, rag=true

2. **Assistant response logging**
   - Receive LLM response
   - Query database: `SELECT * FROM logs WHERE role='assistant' ORDER BY id DESC LIMIT 1`
   - Verify: same sessionid as user prompt, correct content

3. **Session tracking**
   - Send multiple messages in one session
   - Verify all logs share same sessionid
   - Change context/mode (new session)
   - Verify new sessionid in subsequent logs

4. **Database failure handling**
   - Stop PostgreSQL temporarily
   - Send chat message
   - Verify: chat works, error logged, no user-facing error
   - Restart PostgreSQL
   - Verify: subsequent logs succeed

### Manual Testing

**Test Cases:**

- [x] **TC1: Log user prompt in Tutor mode, General Python**
  - Action: Send "What is a variable?" in Tutor mode, General Python
  - Expected: Database row with role=user, context=General Python, mode metadata

- [x] **TC2: Log assistant response in Answer mode, specific assignment**
  - Action: Ask question in Answer mode with Intro-Variables-DataTypes context
  - Expected: Two rows (user + assistant) with same sessionid, correct context

- [x] **TC3: Multiple messages in same session**
  - Action: Send 3 messages without changing context
  - Expected: 6 database rows (3 user + 3 assistant) with same sessionid

- [x] **TC4: New session after context change**
  - Action: Change from Tutor to Answer mode
  - Expected: New sessionid in subsequent logs

- [x] **TC5: Admin vs non-admin user logging**
  - Action: Send messages as admin user, then as roster user
  - Expected: Both logged with correct userid (email)

- [x] **TC6: Long message content**
  - Action: Send very long prompt (>1000 characters)
  - Expected: Full content logged without truncation

- [x] **TC7: Special characters in messages**
  - Action: Send message with emojis, code blocks, quotes
  - Expected: Content stored correctly without escaping issues

## Rollback Plan

**If issues arise after deployment:**

1. **Revert code changes:**
   - Remove logging calls from appnew.py (lines added in v1.0.6)
   - Redeploy previous version (v1.0.5)
   - Database table can remain (no harm in empty table)

2. **Database rollback:**
   - Not necessary (LogModel table created in v1.0.3)
   - If needed to clear test data: `TRUNCATE TABLE logs;`
   - Do NOT drop table (may be needed for v1.0.3+ compatibility)

3. **Configuration rollback:**
   - No configuration changes to revert

4. **Verification after rollback:**
   - Chat functionality works normally
   - No logging errors in application logs
   - Existing logs preserved in database

## References

- Related versions:
  - v1.0.2: Authentication (provides userid)
  - v1.0.3: Database & ChatLogger initialization
  - v1.0.4: LLM integration (provides model metadata)
  - v1.0.5: Context injection (provides context metadata)

- Related files:
  - Implementation: [app/chat/appnew.py](../../../app/chat/appnew.py)
  - Logger: [app/chatlogger.py](../../../app/chatlogger.py)
  - Models: [app/dal/models.py](../../../app/dal/models.py)
  - Requirements: [docs/project_requirements.md](../../project_requirements.md)

- External documentation:
  - SQLModel: https://sqlmodel.tiangolo.com/
  - Loguru: https://loguru.readthedocs.io/

---

**Generated**: 2025-12-27
**Author**: AI-assisted design via /design command
**Version**: 1.0.6
