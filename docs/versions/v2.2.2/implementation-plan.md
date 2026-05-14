# Implementation Plan: Mode Logging in Chat Database - v2.2.2

## Timeline

- **Estimated effort**: 1-2 hours
- **Complexity**: Low
- **Dependencies**: v2.2.1 must be complete

## Phase 1: Preparation

### Tasks

- [ ] Review technical specification ([docs/versions/v2.2.2/technical-spec.md](technical-spec.md))
- [ ] Set up development branch: `feature/v2.2.2-mode-logging`
- [ ] Verify existing `LogModel` structure in `app/dal/models.py`
- [ ] Confirm `st.session_state.mode` is always initialized before log calls in `app.py`
- [ ] Check if `logs` table exists in the target database (new install vs existing)

### Prerequisites

- v2.2.1 complete
- PostgreSQL database accessible
- Admin credentials available for testing

## Phase 2: Backend Implementation — Data Model

### Tasks

- [ ] Add `mode: str` field to `LogModel` in `app/dal/models.py`

### Files to Modify

- `/workspaces/ist256-chatapp/app/dal/models.py`
  - **Changes**: Add `mode: str` field to `LogModel` after the `rag: bool` field (line 91)
  - **Lines**: 84-94 (`LogModel` class body)
  - **Reason**: The database schema must include `mode` before the logger or app layers can write it

### Implementation Detail

```python
class LogModel(SQLModel, table=True):
    __tablename__ = "logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    sessionid: str
    userid: str
    timestamp: str
    model: str
    rag: bool
    mode: str          # ← ADD THIS LINE
    context: str
    role: str
    content: str
```

## Phase 3: Backend Implementation — ChatLogger

### Tasks

- [ ] Update `log()` method signature to accept `mode` between `rag` and `context`
- [ ] Update `LogModel(...)` instantiation inside `log()` to pass `mode=mode`
- [ ] Update `log_user_prompt()` signature: add `mode` parameter after `userid`
- [ ] Update `log_user_prompt()` body: forward `mode` to `log()`
- [ ] Update `log_assistant_response()` signature: add `mode` parameter after `userid`
- [ ] Update `log_assistant_response()` body: forward `mode` to `log()`
- [ ] Update `log_system_prompt()` body: pass `mode="system"` to `log()` (no external signature change)

### Files to Modify

- `/workspaces/ist256-chatapp/app/dal/chatlogger.py`
  - **Changes**: Update `log()`, `log_user_prompt()`, `log_assistant_response()` signatures and bodies; update `log_system_prompt()` internal call
  - **Lines**: 11-35
  - **Reason**: The ChatLogger is the single point where all log entries are constructed and written to the database

### Implementation Detail

```python
def log(self, sessionid, userid, timestamp, model, rag, mode, context, role, content):
    lm = LogModel(
        sessionid=sessionid,
        userid=userid,
        model=model,
        rag=rag,
        mode=mode,          # ← ADD THIS
        context=context,
        timestamp=timestamp,
        role=role,
        content=content
    )
    with self.__db.get_session() as session:
        session.add(lm)
        result = session.commit()
    return result

def log_user_prompt(self, sessionid, userid, mode, context, prompt):     # ← mode added
    return self.log(sessionid, userid, timestamp(), self.__model, self.__rag, mode, context, "user", prompt)

def log_assistant_response(self, sessionid, userid, mode, context, response):  # ← mode added
    return self.log(sessionid, userid, timestamp(), self.__model, self.__rag, mode, context, "assistant", response)

def log_system_prompt(self, appid, userid, system_prompt):               # ← signature unchanged
    return self.log(appid, userid, timestamp(), self.__model, self.__rag, "system", "N/A", "system", system_prompt)
```

## Phase 4: Call Site Update — app.py

### Tasks

- [ ] Update `log_user_prompt()` call to pass `st.session_state.mode` as 3rd argument
- [ ] Update `log_assistant_response()` call to pass `st.session_state.mode` as 3rd argument
- [ ] Verify both calls are inside existing `try/except` blocks (they are — no additional error handling needed)

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/app.py`
  - **Changes**: Insert `st.session_state.mode,` as the 3rd argument in both logging calls
  - **Lines**: ~457-462 (user prompt logging), ~483-488 (assistant response logging)
  - **Streamlit components**: No UI changes — session state read only
  - **Reason**: `st.session_state.mode` holds the user's current mode selection ("Tutor" or "Answer") and must be passed to the logger at the point of logging

### Implementation Detail

**User prompt call site (~line 457):**
```python
st.session_state.chat_logger.log_user_prompt(
    st.session_state.sessionid,
    st.session_state.auth_model.email,
    st.session_state.mode,     # ← ADD THIS LINE
    st.session_state.context,
    prompt
)
```

**Assistant response call site (~line 483):**
```python
st.session_state.chat_logger.log_assistant_response(
    st.session_state.sessionid,
    st.session_state.auth_model.email,
    st.session_state.mode,     # ← ADD THIS LINE
    st.session_state.context,
    full_response
)
```

## Phase 5: Configuration & Constants

### Tasks

- [ ] Update `VERSION = "2.2.2"` in `app/chat/constants.py`
- [ ] No other config file changes needed

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/constants.py`
  - **Changes**: Line 1: Update VERSION
  - **Before**: `VERSION="2.2.1"`
  - **After**: `VERSION="2.2.2"`

## Phase 6: Database Migration (Existing Deployments)

### Tasks

- [ ] For any existing PostgreSQL database, run the following migration SQL **before** deploying the new code:
  ```sql
  ALTER TABLE logs ADD COLUMN mode VARCHAR NOT NULL DEFAULT 'Unknown';
  ```
- [ ] For new installs: no action needed — `SQLModel.metadata.create_all()` creates the column automatically on startup
- [ ] Verify migration success:
  ```sql
  SELECT column_name, data_type FROM information_schema.columns
  WHERE table_name = 'logs' AND column_name = 'mode';
  ```

### Notes

- The `DEFAULT 'Unknown'` ensures historical rows have a valid value
- After migration, new rows will always have an explicit mode value from the application code

## Phase 7: Testing

### Manual Testing Checklist

#### Database Verification
- [ ] Start the app and log in
- [ ] Send a chat message in **Tutor** mode
- [ ] Query database: `SELECT mode, role, content FROM logs ORDER BY id DESC LIMIT 4;`
- [ ] Confirm user and assistant rows both show `mode = 'Tutor'`
- [ ] Switch to **Answer** mode and send another message
- [ ] Confirm new rows show `mode = 'Answer'`
- [ ] Confirm older rows are unchanged (still show previous mode)

#### Export Verification
- [ ] Login as admin; navigate to Admin → Export
- [ ] Export as CSV; open and verify `mode` column is present and populated
- [ ] Export as JSON; verify `mode` field present in each log object

#### Regression Testing
- [ ] App starts without errors
- [ ] Tutor mode chat works end-to-end
- [ ] Answer mode chat works end-to-end
- [ ] Context selection (assignment or General Python) still works
- [ ] Admin pages (Settings, Whitelist, Export, Session) load without error
- [ ] User preferences (mode and context) still persist across sessions

#### Edge Cases
- [ ] First message of a fresh session logs the correct mode
- [ ] Mode logged correctly when context is "General Python" (not just assignments)
- [ ] Both `role = 'user'` and `role = 'assistant'` rows have mode populated
- [ ] VERSION in UI footer shows "2.2.2"

## Phase 8: Documentation

### Tasks

- [ ] Update `docs/versions/README.md` with v2.2.2 entry
- [ ] Update `docs/project_requirements.md` v2.2.2 status to "Released" after deployment
- [ ] No CLAUDE.md changes needed (no new env vars, no new modules, no architectural changes)

### Files to Update

- `/workspaces/ist256-chatapp/docs/versions/README.md`
  - **Changes**: Add v2.2.2 row to version table (latest first)

- `/workspaces/ist256-chatapp/docs/project_requirements.md`
  - **Changes**: Update Status to "Released" and set Release Date after deployment

## Phase 9: Deployment

### Tasks

- [ ] Run SQL migration on target database (if existing install)
- [ ] Commit changes: `"Implement v2.2.2: Add mode field to chat logs"`
- [ ] Push feature branch to remote
- [ ] Create PR to main branch
- [ ] Code review
- [ ] Merge to main
- [ ] Verify CI/CD pipeline passes
- [ ] Monitor deployment logs for errors

### Deployment Checklist

- [ ] SQL migration run on target database
- [ ] All manual tests passing locally
- [ ] No merge conflicts with main
- [ ] VERSION constant updated to "2.2.2"
- [ ] `mode` field in `LogModel`
- [ ] `mode` parameter in `log_user_prompt()` and `log_assistant_response()`
- [ ] Both call sites in `app.py` pass `st.session_state.mode`
- [ ] No errors in local test run
- [ ] Export shows `mode` column

## Dependencies

### Internal Dependencies

- **v2.2.1** (Whitelist refactoring) must be complete
- PostgreSQL `logs` table must exist (created by existing deployment)
- `st.session_state.mode` must be initialized before chat logging (confirmed — initialized at session start from user preferences)

### External Dependencies

None — uses existing libraries (sqlmodel, streamlit, loguru)

### Blocked By

Nothing — all prerequisites are in place

## Risks & Mitigation

### Risk 1: SQL migration not run before deploying to existing database

- **Impact**: High — all chat log inserts fail with `UndefinedColumn` error; chat still works but nothing is logged
- **Probability**: Medium — easy to forget the migration step
- **Mitigation**:
  - Document migration prominently in deployment checklist
  - Existing `try/except` in app.py prevents user-visible crash; logs the error
  - Migration is a single `ALTER TABLE` statement — fast and low-risk

### Risk 2: `st.session_state.mode` not yet initialized when logging

- **Impact**: Medium — `KeyError` at log call site
- **Probability**: Very Low — `mode` is set during session initialization (before any chat is possible)
- **Mitigation**:
  - Existing session initialization code always sets mode from user preferences or defaults
  - Existing `try/except` at log call sites catches and logs any such error

## Success Criteria

- [ ] `LogModel` has `mode: str` field
- [ ] `log_user_prompt()` and `log_assistant_response()` accept `mode` parameter
- [ ] Both log call sites in `app.py` pass `st.session_state.mode`
- [ ] `SELECT mode FROM logs` returns `'Tutor'` or `'Answer'` for new rows
- [ ] CSV and JSON exports include the `mode` field
- [ ] No errors in application logs after deployment
- [ ] VERSION displays "2.2.2" in UI footer
- [ ] All regression tests pass

## Rollback Procedure

1. **Identify issue** — check application logs for `UndefinedColumn` or `TypeError` exceptions
2. **Revert code**: `git revert <v2.2.2-commit-hash>`
3. **Drop column** (only if migration was applied):
   ```sql
   ALTER TABLE logs DROP COLUMN mode;
   ```
4. **Verify rollback** — chat messages log without error; no `mode` column in export

## Post-Deployment

### Monitoring

- Watch application logs for database errors in the first 24 hours
- Spot-check the `logs` table to confirm `mode` is populated correctly

### Key Metrics

- Zero `UndefinedColumn` or `TypeError` exceptions in logs
- `mode` column non-null for all new log rows

### Follow-up Tasks

- [ ] Consider adding a database index on `mode` in a future version to support analytics queries
- [ ] Consider adding `mode` to the session debug page display

---

**Generated**: 2026-02-20
**Author**: AI-assisted planning via /design command
**Version**: 2.2.2
