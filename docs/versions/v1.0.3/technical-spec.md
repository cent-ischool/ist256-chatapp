# Technical Specification: Database & Logging Infrastructure - v1.0.3

## Overview

Version 1.0.3 establishes the database connection and chat logging infrastructure for appnew.py. This version initializes the PostgreSQL database connection and creates a ChatLogger instance, preparing the foundation for comprehensive chat interaction logging that will be fully utilized in v1.0.6. This is a critical infrastructure step in the v2.0 migration, enabling data persistence and analytics capabilities.

## Architecture Changes

### Components Affected

- `/workspaces/ist256-chatapp/app/chat/appnew.py` - Add database and ChatLogger initialization
- `/workspaces/ist256-chatapp/app/chat/constants.py` - Update VERSION to "1.0.3"

### New Components

No new files created. All infrastructure integrated into existing appnew.py.

### Dependencies

**External Libraries** (already in requirements.txt):
- `sqlalchemy` - SQL toolkit and ORM
- `sqlmodel` - Pydantic-based ORM combining SQLAlchemy + Pydantic
- `psycopg2` - PostgreSQL database adapter

**Internal Modules**:
- `/workspaces/ist256-chatapp/app/dal/db.py` - PostgresDb class
- `/workspaces/ist256-chatapp/app/dal/models.py` - LogModel schema
- `/workspaces/ist256-chatapp/app/chatlogger.py` - ChatLogger class

## Data Models

### Database Changes

**No schema changes required.** Uses existing LogModel schema:

```python
class LogModel(SQLModel, table=True):
    __tablename__ = "logs"

    id: int (Primary Key, auto-increment)
    sessionid: str  # User session UUID
    userid: str     # User email
    timestamp: str  # ISO format timestamp
    model: str      # LLM model name
    rag: bool       # RAG enabled flag
    context: str    # Assignment/context name
    role: str       # "user", "assistant", or "system"
    content: str    # Message text
```

Database already exists at `DATABASE_URL` environment variable location.

### API Changes

No API changes. Database is accessed via PostgresDb ORM wrapper.

## Technical Design

### Backend Implementation

**Database Initialization** (from app.py lines 147-149):

```python
if 'db' not in st.session_state:
    db = PostgresDb(os.environ["DATABASE_URL"])
    st.session_state.db = db
```

**ChatLogger Initialization** (from app.py line 202):

```python
# Note: This happens AFTER LLM initialization in app.py
# For v1.0.3, we prepare ChatLogger but won't use it until v1.0.6
chat_logger = ChatLogger(
    st.session_state.db,
    model="mocked",  # Placeholder until v1.0.4 adds real LLM
    rag=True         # Always true in v2.0 (context always on)
)
st.session_state.chat_logger = chat_logger
```

**PostgresDb Class** (from dal/db.py):
- Manages SQLAlchemy engine and session
- Provides create_tables() method for schema initialization
- Handles connection pooling
- Thread-safe session management

**ChatLogger Class** (from chatlogger.py):
- Constructor takes: db, model name, RAG flag
- Methods:
  - `log_user_prompt(sessionid, userid, context, content)` - Logs user messages
  - `log_assistant_response(sessionid, userid, context, content)` - Logs AI responses
  - Creates LogModel entries with timestamp
  - Automatically commits to database

### Frontend Implementation

No UI changes. Database initialization happens behind the scenes before chat interface loads.

### Integration Points

**Session State Integration**:
- `st.session_state.db` - PostgreSQL connection (available throughout app)
- `st.session_state.chat_logger` - ChatLogger instance (ready for v1.0.6)
- `st.session_state.sessionid` - UUID from set_context() (already exists from v1.0.2)
- `st.session_state.auth_model.email` - User email (from v1.0.2)

**No LLM Integration** yet - model name will be placeholder until v1.0.4

**No Actual Logging** yet - infrastructure prepared but logging calls added in v1.0.6

## Configuration

### Environment Variables

**Required:**

- `DATABASE_URL` - PostgreSQL connection string
  - Format: `postgresql://user:password@host:port/database`
  - Example: `postgresql://pgadmin:password@nas.home.michaelfudge.com:15432/ist256chatlogs`

**No new environment variables** for this version.

### Config Files

No changes to config.yaml or prompts.yaml.

## Security Considerations

**Database Security**:
- Connection string contains credentials (keep in .env, not code)
- Use environment variables for DATABASE_URL
- PostgreSQL user should have limited permissions (no DROP/ALTER)

**Data Privacy**:
- User emails stored in logs (PII consideration)
- Session IDs are UUIDs (non-guessable)
- Message content stored as-is (no encryption at rest)
- Chat logs accessible to admins via database queries

**SQL Injection Prevention**:
- SQLModel/SQLAlchemy provides parameterized queries
- No raw SQL execution in ChatLogger
- ORM prevents injection attacks

## Performance Considerations

**Database Performance**:
- Connection pooling via SQLAlchemy
- Single connection per Streamlit session
- Minimal overhead (~10ms per log write)

**Scalability**:
- PostgreSQL can handle thousands of concurrent sessions
- Database on separate server (nas.home.michaelfudge.com)
- No indexes needed initially (small dataset)

**Memory Usage**:
- Database connection: ~1MB per session
- ChatLogger instance: ~1KB per session
- Negligible impact on Streamlit memory

**No Performance Impact** on chat interface (logging is asynchronous to user interaction)

## Error Handling

**Expected Errors**:

1. **Database connection failure**:
   - Error: `psycopg2.OperationalError` or connection timeout
   - Action: Display error in sidebar, stop app
   - User message: "Database unavailable. Please contact support."

2. **Missing DATABASE_URL**:
   - Error: `KeyError` on environment variable
   - Action: App crashes with clear error
   - Admin must configure environment

3. **Database schema mismatch**:
   - Error: SQLAlchemy table not found
   - Action: Call db.create_tables() if needed
   - Log warning if schema auto-created

4. **Log write failure**:
   - Error: Database constraint violation or timeout
   - Action: Log error but don't crash chat interface
   - User continues chatting, logs missed

**Error Recovery**:
- Database errors don't crash the app
- Chat functionality continues even if logging fails
- Errors logged to console via loguru

**User-Facing Messages**:
- Simple, clear error messages
- No technical jargon or SQL errors exposed
- Suggest contacting instructor/admin

## Testing Strategy

### Manual Testing

- [ ] **Database connection successful**
  - Verify DATABASE_URL is set
  - Verify PostgresDb initializes without error
  - Check st.session_state.db exists

- [ ] **ChatLogger initialization**
  - Verify ChatLogger created with placeholder model
  - Check st.session_state.chat_logger exists
  - Verify RAG flag set to True

- [ ] **Session persistence**
  - Refresh page after database init
  - Verify db connection persists in session
  - No re-initialization on refresh

- [ ] **Missing DATABASE_URL**
  - Remove DATABASE_URL from .env temporarily
  - Verify clear KeyError message
  - Restore environment variable

- [ ] **Database unreachable**
  - Stop PostgreSQL server temporarily
  - Verify connection error handled gracefully
  - Restart database

- [ ] **No logging calls yet**
  - Verify chat interface works normally
  - Confirm no log entries created (until v1.0.6)

### Integration Testing

- [ ] **PostgreSQL integration**
  - Connect to database manually
  - Verify logs table exists
  - Check connection pooling works

- [ ] **Session state integration**
  - Verify db and chat_logger in session
  - Test with authenticated user (from v1.0.2)
  - Confirm sessionid available from set_context()

### Edge Cases

- [ ] Database credentials incorrect
- [ ] PostgreSQL server down
- [ ] Network timeout to database
- [ ] Database disk full
- [ ] Multiple concurrent sessions

## Rollback Plan

### Rollback Procedure

1. **Revert appnew.py changes**:
   ```bash
   git revert <commit-hash>
   git push origin ui-upgrade
   ```

2. **No database cleanup needed**:
   - No schema changes made
   - No data written yet
   - Database unchanged

3. **Clear session state** (if needed):
   - Users clear browser cache
   - Or restart Streamlit app

4. **Verify old app.py still works**:
   - app.py unchanged, should remain functional
   - Fallback option for users

No database migration rollback needed.

## References

- PostgreSQL Connection: `/workspaces/ist256-chatapp/app/dal/db.py`
- ChatLogger Implementation: `/workspaces/ist256-chatapp/app/chatlogger.py`
- Log Schema: `/workspaces/ist256-chatapp/app/dal/models.py` (LogModel)
- Existing Implementation: `/workspaces/ist256-chatapp/app/chat/app.py` lines 147-149, 202

---

**Generated**: 2025-12-27
**Author**: AI-assisted design via manual /design execution
**Version**: 1.0.3
