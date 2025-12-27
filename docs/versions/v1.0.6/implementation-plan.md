# Implementation Plan: Chat Logging - v1.0.6

## Timeline

- Estimated effort: 2-3 hours
- Complexity: Low
- Suggested sprint: Can be completed in single focused work session

## Phase 1: Preparation

### Tasks

- [ ] Review technical specification: `/workspaces/ist256-chatapp/docs/versions/v1.0.6/technical-spec.md`
- [ ] Set up development branch: `feature/v1.0.6-chat-logging`
- [ ] Update TODO.txt with version tasks
- [ ] Verify all dependencies are available (v1.0.2-v1.0.5 complete)
- [ ] Review existing ChatLogger implementation in `/workspaces/ist256-chatapp/app/chatlogger.py`
- [ ] Review existing logging pattern in `/workspaces/ist256-chatapp/app/chat/app.py` (lines 246-247, 263-264)

### Prerequisites

- v1.0.2 complete: Authentication provides `st.session_state.auth_model.email`
- v1.0.3 complete: ChatLogger initialized in `st.session_state.chat_logger`
- v1.0.4 complete: LLM provides model metadata via `st.session_state.config.ai_model`
- v1.0.5 complete: Context available in `st.session_state.context`
- PostgreSQL database accessible and LogModel table exists
- Verify with: `psql $DATABASE_URL -c "SELECT COUNT(*) FROM logs;"`

## Phase 2: Backend Implementation

### Tasks

- [ ] Add user prompt logging after line 315 in appnew.py
- [ ] Add assistant response logging after line 329 in appnew.py
- [ ] Add error handling (try/except) around both logging calls
- [ ] Add loguru debug logging for successful log calls
- [ ] Add loguru error logging for failed log calls

### Files to Modify

#### `/workspaces/ist256-chatapp/app/chat/appnew.py`

**Change 1: User Prompt Logging (after line 315)**
- **Location**: After `st.session_state.messages.append({"role": "user", "content": prompt})`
- **Lines**: Insert after line 315
- **Changes**: Add logging call with error handling
- **Code to add**:
```python
# Log user prompt to database (v1.0.6)
try:
    st.session_state.chat_logger.log_user_prompt(
        st.session_state.sessionid,
        st.session_state.auth_model.email,
        st.session_state.context,
        prompt
    )
    logger.debug(f"Logged user prompt: session={st.session_state.sessionid}, context={st.session_state.context}")
except Exception as e:
    logger.error(f"Failed to log user prompt: {e}")
```

**Change 2: Assistant Response Logging (after line 329)**
- **Location**: After `st.session_state.messages.append({"role": "assistant", "content": full_response})`
- **Lines**: Insert after line 329
- **Changes**: Add logging call with error handling
- **Code to add**:
```python
# Log assistant response to database (v1.0.6)
try:
    st.session_state.chat_logger.log_assistant_response(
        st.session_state.sessionid,
        st.session_state.auth_model.email,
        st.session_state.context,
        full_response
    )
    logger.debug(f"Logged assistant response: session={st.session_state.sessionid}, context={st.session_state.context}")
except Exception as e:
    logger.error(f"Failed to log assistant response: {e}")
```

**Reason**: These changes enable complete chat logging while maintaining graceful degradation if database unavailable.

### Files to Create

None. All required components already exist.

## Phase 3: Frontend Implementation

### Tasks

- [ ] No UI changes required

### Files to Modify

None. Logging is transparent to the user.

### Files to Create

None.

## Phase 4: Configuration & Constants

### Tasks

- [ ] Update `app/chat/constants.py` with VERSION = "1.0.6"
- [ ] No other configuration changes needed

### Configuration Changes

#### `/workspaces/ist256-chatapp/app/chat/constants.py`

- **Change**: Update line 1 from `VERSION="1.0.5"` to `VERSION="1.0.6"`
- **Reason**: Reflect current version in UI footer

#### No changes to:
- `/workspaces/ist256-chatapp/app/data/config.yaml`
- `/workspaces/ist256-chatapp/app/data/prompts.yaml`
- Environment variables

## Phase 5: Testing

### Tasks

- [ ] Manual testing checklist
  - [ ] TC1: Log user prompt in Tutor mode, General Python
  - [ ] TC2: Log assistant response in Answer mode, specific assignment
  - [ ] TC3: Multiple messages in same session (verify same sessionid)
  - [ ] TC4: New session after context change (verify new sessionid)
  - [ ] TC5: Admin vs non-admin user logging (verify both work)
  - [ ] TC6: Long message content (>1000 characters)
  - [ ] TC7: Special characters in messages (emojis, code blocks, quotes)
  - [ ] TC8: Database failure handling (stop PostgreSQL, verify graceful degradation)
- [ ] Integration testing
  - [ ] Database integration: Query logs table to verify data
  - [ ] Session tracking: Verify sessionid consistency within session
  - [ ] Context tracking: Verify context matches selection
- [ ] Performance testing
  - [ ] Verify no noticeable latency added to chat responses
  - [ ] Send 10 rapid messages, verify all logged

### Test Data

**Database Queries for Verification:**

```sql
-- View recent logs
SELECT * FROM logs ORDER BY id DESC LIMIT 10;

-- Count logs by role
SELECT role, COUNT(*) FROM logs GROUP BY role;

-- View logs for specific session
SELECT sessionid, role, context, LEFT(content, 50) as preview, timestamp
FROM logs
WHERE sessionid = '<session-uuid>'
ORDER BY timestamp;

-- View logs for specific user
SELECT role, context, LEFT(content, 50) as preview, timestamp
FROM logs
WHERE userid = 'user@syr.edu'
ORDER BY timestamp DESC
LIMIT 20;

-- Verify RAG flag (should all be true in v2.0)
SELECT rag, COUNT(*) FROM logs GROUP BY rag;
```

**Test User Accounts:**
- Admin user: Use email from `ADMIN_USERS` env var
- Roster user: Use email from roster file
- Verify both types log correctly

### Detailed Test Case Execution

**TC1: Log user prompt in Tutor mode, General Python**
1. Open appnew.py
2. Set Mode: Tutor, Context: General Python
3. Send message: "What is a variable?"
4. Query database: `SELECT * FROM logs WHERE role='user' ORDER BY id DESC LIMIT 1;`
5. Verify:
   - `role = 'user'`
   - `context = 'General Python'`
   - `content = 'What is a variable?'`
   - `rag = true`
   - `userid` matches your email
   - `sessionid` is valid UUID4
   - `timestamp` is recent ISO 8601 UTC

**TC2: Log assistant response in Answer mode, specific assignment**
1. Change to Answer mode, select "Intro-Variables-DataTypes"
2. Send message: "Explain string concatenation"
3. Wait for response
4. Query database: `SELECT * FROM logs WHERE role IN ('user', 'assistant') ORDER BY id DESC LIMIT 2;`
5. Verify:
   - Two rows: one user, one assistant
   - Both have same `sessionid`
   - Both have `context = 'Intro-Variables-DataTypes'`
   - User content matches prompt, assistant content matches response

**TC3: Multiple messages in same session**
1. Without changing mode/context, send 3 messages
2. Query database: `SELECT sessionid, role FROM logs ORDER BY id DESC LIMIT 6;`
3. Verify:
   - 6 rows total
   - All have same `sessionid`
   - Alternating user/assistant roles

**TC4: New session after context change**
1. Note current sessionid from logs
2. Change mode from Tutor to Answer (triggers new session)
3. Send message
4. Query database and verify new sessionid different from previous

**TC5: Database failure handling**
1. Stop PostgreSQL: `docker-compose stop postgres` (or equivalent)
2. Send chat message in appnew.py
3. Verify:
   - Chat still works and displays response
   - Application logs show error: "Failed to log user prompt"
   - No user-facing error message
4. Restart PostgreSQL: `docker-compose start postgres`
5. Send another message
6. Verify logging resumes successfully

## Phase 6: Documentation

### Tasks

- [ ] Update CLAUDE.md if architecture details changed (likely no changes needed)
- [ ] Update README.md if user-facing changes (no user-facing changes)
- [ ] Add inline code comments for logging calls (v1.0.6 marker comments)
- [ ] No deployment documentation changes needed
- [ ] No new environment variables to document
- [ ] Update version in docs/versions/README.md (done automatically by /design)

### Documentation Files

#### `/workspaces/ist256-chatapp/CLAUDE.md`

**Optional Update: Chat Flow Section**
- **Location**: Line 36 "Chat Flow (v1.0.5+)"
- **Change**: Update to "Chat Flow (v1.0.6+)" and add logging step
- **New text to add** (after step 5):
```
6. Both user prompt and assistant response logged to PostgreSQL (v1.0.6+)
```

**Optional Update: Database Schema Section**
- **Location**: Around line 79 "Database Schema"
- **Change**: Add note about logging
- **New text to add**:
```
All chat messages are logged (v1.0.6+) with full context metadata for analytics.
```

#### Inline Code Comments

Add version marker comments in appnew.py:
```python
# Log user prompt to database (v1.0.6)
try:
    st.session_state.chat_logger.log_user_prompt(...)
```

## Phase 7: Deployment

### Tasks

- [ ] Commit changes with message: "Implement v1.0.6: Chat logging to database"
- [ ] Push feature branch to remote
- [ ] Create PR to main branch
- [ ] Code review: Verify error handling, verify no blocking database calls
- [ ] Address review feedback if any
- [ ] Merge to main
- [ ] Verify CI/CD pipeline passes (GitHub Actions build)
- [ ] Monitor deployment logs for errors
- [ ] Verify in production: Query logs table to confirm messages being logged

### Deployment Checklist

- [ ] All tests passing (manual tests completed)
- [ ] No merge conflicts with main
- [ ] Version number updated to 1.0.6 in constants.py
- [ ] Documentation complete (technical-spec.md, implementation-plan.md)
- [ ] No breaking changes (backward compatible)
- [ ] Database table exists (created in v1.0.3)
- [ ] Error handling prevents chat failures on DB issues

### Commit Message Template

```
Implement v1.0.6: Chat logging to database

Add comprehensive logging of all user prompts and assistant responses
to PostgreSQL database for analytics and audit trails.

Changes:
- Add chat_logger.log_user_prompt() call in appnew.py after user input
- Add chat_logger.log_assistant_response() call after LLM response
- Include error handling to prevent chat failures on DB issues
- Update VERSION to 1.0.6 in constants.py
- Add debug logging for successful log operations

Features:
- All messages logged with mode, context, sessionid, model metadata
- RAG flag always true (context always available in v2.0)
- Graceful degradation if database unavailable
- No user-facing changes (transparent logging)

Testing:
- Manual testing: All 8 test cases passed
- Database integration verified
- Session tracking confirmed
- Error handling tested (DB failure scenario)

Dependencies: v1.0.2, v1.0.3, v1.0.4, v1.0.5
Complexity: Low | Effort: 2-3 hours
```

## Dependencies

### Internal Dependencies

**Must be complete before starting v1.0.6:**
- ✅ v1.0.2: Authentication & Authorization (provides userid)
- ✅ v1.0.3: Database & Logging Infrastructure (ChatLogger initialized)
- ✅ v1.0.4: LLM Integration (provides model metadata)
- ✅ v1.0.5: Context Injection (provides context metadata)

### External Dependencies

- PostgreSQL database accessible at `DATABASE_URL`
- LogModel table exists (created in v1.0.3)
- SQLModel/SQLAlchemy installed (in requirements.txt)

### Team Dependencies

None. Single developer can implement this feature independently.

## Risks & Mitigation

### Risk 1: Database Performance Degradation

- **Impact**: Medium
- **Probability**: Low
- **Description**: Two additional database INSERTs per chat exchange could slow response time
- **Mitigation**:
  - Logging is asynchronous from user perspective (happens after response displayed)
  - Single-row inserts are very fast (<10ms)
  - Error handling prevents blocking on DB issues
  - Monitor database performance after deployment
  - Future: Consider async logging queue if needed (not needed now)

### Risk 2: Database Connection Failures

- **Impact**: Low (chat continues working)
- **Probability**: Low
- **Description**: Database unavailable or connection pool exhausted
- **Mitigation**:
  - Try/except blocks prevent chat failures
  - Errors logged to application logs for monitoring
  - Graceful degradation: chat works, logging skipped
  - Database connection pooling handled by SQLModel

### Risk 3: Disk Space for Logs

- **Impact**: Low (long-term concern)
- **Probability**: Medium (over months/years)
- **Description**: logs table grows indefinitely
- **Mitigation**:
  - Short-term: Not a concern (course is one semester)
  - Long-term: Implement archiving/partitioning strategy
  - Monitor database size monthly
  - Plan retention policy (e.g., keep 1 year, archive older)

### Risk 4: Incomplete Session State

- **Impact**: Medium (logging fails)
- **Probability**: Very Low
- **Description**: `chat_logger`, `sessionid`, or `auth_model` missing from session state
- **Mitigation**:
  - These are initialized early in appnew.py flow (v1.0.2, v1.0.3)
  - Error handling catches AttributeError if missing
  - Add defensive checks if needed: `if 'chat_logger' in st.session_state:`

### Risk 5: Sensitive Data in Logs

- **Impact**: Medium (privacy concern)
- **Probability**: High (students will share code/answers)
- **Description**: Student prompts may contain assignment solutions or personal info
- **Mitigation**:
  - Database access restricted to service account
  - No user-facing interface to view others' logs
  - Follow university data retention policies
  - Document in privacy policy (if exists)
  - Future: Implement admin analytics with appropriate access controls

## Success Criteria

- [ ] All tasks in phases 1-7 completed
- [ ] Version number updated to 1.0.6 in constants.py
- [ ] All 8 manual test cases passing
- [ ] Documentation updated (technical spec, implementation plan)
- [ ] Code reviewed and approved
- [ ] Deployed to production (merged to main)
- [ ] No critical bugs reported within 24 hours of deployment
- [ ] Feature functions as specified in requirements:
  - [ ] User prompts logged to database
  - [ ] Assistant responses logged to database
  - [ ] Logs include mode, context, sessionid, model, RAG flag
  - [ ] Graceful degradation on database failures
- [ ] Database queries confirm logs being written:
  - [ ] `SELECT COUNT(*) FROM logs;` shows increasing count
  - [ ] Logs have correct sessionid, userid, context, role, content

## Rollback Procedure

### If Critical Issues Arise

**Scenario 1: Database Performance Issues**
1. Revert logging code changes in appnew.py
2. Commit: `git revert <commit-hash> -m "Rollback v1.0.6: Database performance issues"`
3. Push to main
4. Deploy immediately
5. Verify chat works without logging
6. Investigate performance issue (indexes, connection pooling)
7. Re-implement with optimizations

**Scenario 2: Chat Failures Due to Logging**
1. Immediate rollback: Revert to v1.0.5
2. Check error logs: `grep "Failed to log" application.log`
3. Identify root cause (DB connection, session state, etc.)
4. Fix error handling in code
5. Re-test locally
6. Re-deploy with improved error handling

**Scenario 3: Data Privacy Concern**
1. Do NOT rollback code (chat already logged)
2. Implement access controls on logs table
3. Review and redact sensitive data if needed
4. Update privacy policy
5. Communicate with affected users if required

### Verification After Rollback

1. Chat functionality works normally (send test message)
2. No logging errors in application logs
3. Existing logs preserved in database (verify with query)
4. Application version updated in constants.py if needed
5. Monitoring shows normal performance metrics

### Database Cleanup (if needed)

```sql
-- Clear all logs (use with caution!)
TRUNCATE TABLE logs;

-- Clear logs for specific session
DELETE FROM logs WHERE sessionid = '<session-uuid>';

-- Clear logs for test users
DELETE FROM logs WHERE userid IN ('test@example.com', 'test2@example.com');
```

## Post-Deployment

### Monitoring

**What to Monitor (first 24-48 hours):**

1. **Application Logs** (loguru output):
   - Watch for: "Failed to log user prompt" or "Failed to log assistant response"
   - Expected: Minimal or no errors
   - Alert threshold: >5 errors per hour indicates systemic issue

2. **Database Metrics**:
   - Query: `SELECT COUNT(*) FROM logs;` hourly
   - Expected: Steady growth proportional to chat activity
   - Watch for: No growth (logging broken) or excessive growth (duplicate logs)

3. **Response Time**:
   - User-perceived chat latency
   - Expected: No noticeable change from v1.0.5
   - Alert threshold: >500ms increase in average response time

4. **Database Connection Pool**:
   - Monitor PostgreSQL connection count
   - Expected: Stable, within pool limits
   - Alert threshold: Connection pool exhaustion

5. **Disk Space**:
   - Monitor database volume usage
   - Expected: Slow, linear growth
   - Alert threshold: >80% capacity (plan archiving)

### Key Metrics to Watch

```sql
-- Messages logged per hour
SELECT DATE_TRUNC('hour', timestamp::timestamp) as hour, COUNT(*)
FROM logs
GROUP BY hour
ORDER BY hour DESC
LIMIT 24;

-- Messages by user
SELECT userid, COUNT(*) as message_count
FROM logs
GROUP BY userid
ORDER BY message_count DESC
LIMIT 10;

-- Messages by context
SELECT context, COUNT(*) as message_count
FROM logs
GROUP BY context
ORDER BY message_count DESC;

-- Average messages per session
SELECT AVG(msg_count) as avg_messages_per_session
FROM (
    SELECT sessionid, COUNT(*) as msg_count
    FROM logs
    GROUP BY sessionid
) session_counts;
```

### Follow-up Tasks

- [ ] Add database indexes for analytics queries (future optimization):
  - `CREATE INDEX idx_logs_userid ON logs(userid);`
  - `CREATE INDEX idx_logs_timestamp ON logs(timestamp);`
  - `CREATE INDEX idx_logs_sessionid ON logs(sessionid);`

- [ ] Document database retention policy (future work)

- [ ] Implement admin analytics dashboard (v1.0.7 or later):
  - View logs for specific user
  - View logs for specific session
  - Aggregate statistics (most asked questions, popular contexts, etc.)

- [ ] Consider async logging queue if performance issues arise (unlikely):
  - Use Celery or similar task queue
  - Decouple logging from chat flow
  - Batch inserts for efficiency

- [ ] Plan data archiving strategy for multi-year deployments:
  - Archive logs older than 1 year to separate table
  - Implement log rotation
  - Export to data warehouse for long-term analytics

---

**Generated**: 2025-12-27
**Author**: AI-assisted planning via /design command
**Version**: 1.0.6
