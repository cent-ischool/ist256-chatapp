# Technical Specification: User Preferences Persistence - v1.0.10

## Overview

This feature implements persistent storage of user preferences (mode and context) in PostgreSQL, allowing users' AI mode and context selections to persist across sessions. When a user logs in, their previously selected preferences are automatically restored. When they change mode or context and click "Save + New Chat" or "Reset to Defaults", their preferences are updated in the database.

## Architecture Changes

### Components Affected

- `/workspaces/ist256-chatapp/app/chat/appnew.py`
  - Load user preferences on authentication
  - Save preferences when mode/context changes
- `/workspaces/ist256-chatapp/app/dal/db.py`
  - Import UserPreferencesModel for table creation
- `/workspaces/ist256-chatapp/app/dal/models.py`
  - UserPreferencesModel already exists (lines 65-69)

### New Components

- `/workspaces/ist256-chatapp/app/dal/user_preferences.py`
  - Data access layer for user preferences operations
  - Functions: `get_preferences(user_email)`, `save_preferences(user_email, mode, context)`

### Dependencies

- `sqlmodel` - Already in requirements.txt for ORM operations
- `loguru` - Already in requirements.txt for logging
- No new external dependencies required

## Data Models

### Database Changes

**Existing Model: UserPreferencesModel** (already defined in `/workspaces/ist256-chatapp/app/dal/models.py:65-69`)

```python
class UserPreferencesModel(SQLModel, table=True):
    __tablename__ = "user_preferences"
    user_email: str = Field(default=None, primary_key=True)
    mode: str = "Tutor"
    context: str = "General Python"
```

**Table Creation:**
- Table will be auto-created via SQLModel.metadata.create_all() in PostgresDb.__init__()
- Need to import UserPreferencesModel in `/workspaces/ist256-chatapp/app/dal/db.py:6`

**No schema migration needed** - SQLModel handles table creation automatically

### API Changes

**New module: app/dal/user_preferences.py**

Function signatures:
```python
def get_preferences(db: PostgresDb, user_email: str) -> Optional[UserPreferencesModel]:
    """
    Retrieve user preferences from database.
    Returns None if no preferences found (first-time user).
    """

def save_preferences(db: PostgresDb, user_email: str, mode: str, context: str) -> UserPreferencesModel:
    """
    Save or update user preferences in database.
    Creates new record if doesn't exist, updates if exists.
    """
```

## Technical Design

### Backend Implementation

**app/dal/user_preferences.py:**
1. Import required modules: PostgresDb, UserPreferencesModel, SQLModel select
2. Implement `get_preferences()`:
   - Open database session using `db.get_session()`
   - Query user_preferences table for user_email
   - Return UserPreferencesModel if found, None otherwise
   - Handle database exceptions with try/except
   - Log retrieval with loguru
3. Implement `save_preferences()`:
   - Open database session
   - Check if preferences exist for user_email
   - If exists: update mode and context fields
   - If not exists: create new UserPreferencesModel record
   - Commit changes
   - Return saved model
   - Handle database exceptions
   - Log save operation

**Error Handling Strategy:**
- Database connection errors: Log error, return None/defaults
- Constraint violations: Log error, graceful fallback
- Invalid email: Should not occur (validated by auth), but check for empty string

### Frontend Implementation

**app/chat/appnew.py modifications:**

**1. Load preferences after authentication (after line 263):**
```python
# After successful authentication and authorization
from dal.user_preferences import get_preferences

if 'preferences_loaded' not in st.session_state:
    try:
        prefs = get_preferences(st.session_state.db, st.session_state.auth_model.email)
        if prefs:
            # Load saved preferences
            set_context(prefs.mode, prefs.context)
            logger.info(f"Loaded user preferences: email={email}, mode={prefs.mode}, context={prefs.context}")
        else:
            # First-time user, use defaults
            set_context("Tutor", "General Python")
            logger.info(f"New user, using defaults: email={email}")
    except Exception as e:
        logger.error(f"Failed to load preferences for {email}: {e}")
        set_context("Tutor", "General Python")  # Fallback to defaults

    st.session_state.preferences_loaded = True
```

**2. Save preferences when mode/context changes (around line 488-493):**
```python
from dal.user_preferences import save_preferences

if set_mode:
    # Save preferences before setting new context
    try:
        save_preferences(st.session_state.db, st.session_state.auth_model.email, mode, context)
        logger.info(f"Saved preferences: email={st.session_state.auth_model.email}, mode={mode}, context={context}")
    except Exception as e:
        logger.error(f"Failed to save preferences: {e}")

    set_context(mode, context)
    st.rerun()

elif reset_to_defaults:
    # Save default preferences
    try:
        save_preferences(st.session_state.db, st.session_state.auth_model.email, "Tutor", "General Python")
        logger.info(f"Reset preferences to defaults: email={st.session_state.auth_model.email}")
    except Exception as e:
        logger.error(f"Failed to save default preferences: {e}")

    set_context("Tutor", "General Python")
    st.rerun()
```

### Integration Points

**PostgreSQL Database:**
- Uses existing PostgresDb connection in session state
- Table auto-created on startup via SQLModel.metadata.create_all()
- CRUD operations via SQLModel ORM

**Authentication System:**
- Preferences loaded after successful MSAL authentication
- user_email from AuthModel.email used as primary key
- Scoped per user - no cross-user access

**Session State Management:**
- `preferences_loaded` flag prevents re-loading on every rerun
- Integrates with existing `set_context()` function
- Works with existing mode/context UI controls

**Streamlit Lifecycle:**
- Load preferences once per session after auth
- Save preferences on user action (button clicks)
- No automatic saves on selection change (prevents unwanted persistence)

## Configuration

### Environment Variables

No new environment variables required.

### Config Files

No changes to config.yaml, prompts.yaml, or constants.py needed for this feature.

## Security Considerations

**Authentication:**
- User must be authenticated via MSAL before preferences can be loaded
- Preferences only accessible after authorization check passes

**Authorization/Access Control:**
- Users can only access their own preferences (user_email as primary key)
- No admin-specific functionality - all authenticated users get this feature

**Data Privacy:**
- user_email stored as identifier (PII, but required for feature)
- mode and context are not sensitive (just "Tutor"/"Answer" and assignment names)
- No additional PII collected

**Input Validation:**
- mode: Must be one of const.MODES ("Tutor", "Answer")
- context: Must be in context_list (validated assignments or "General Python")
- user_email: Already validated by MSAL authentication

**SQL Injection Prevention:**
- Using SQLModel ORM with parameterized queries
- No raw SQL execution
- user_email passed as parameter, not concatenated

**XSS Prevention:**
- No user input rendered as HTML
- Preferences values are controlled (not arbitrary strings)

## Performance Considerations

**Scalability:**
- Single row per user in user_preferences table
- Primary key on user_email for fast lookups
- Minimal table size growth (1 row per user)
- No indexing needed beyond primary key

**Caching:**
- Preferences loaded once per session and stored in session state
- No repeated database queries during session
- Only writes on explicit user action

**Database Query Optimization:**
- Simple primary key lookups (O(1) with index)
- Upsert pattern minimizes queries
- No joins or complex queries

**Memory Usage:**
- Negligible - single UserPreferencesModel per user session
- Model contains only 3 strings

## Error Handling

**Expected Errors:**

1. **Database connection failure during load:**
   - User sees: No error message (silent fallback)
   - Behavior: Defaults to "Tutor" and "General Python"
   - Logging: Error logged with user email and exception

2. **Database connection failure during save:**
   - User sees: No error message (preferences saved in session)
   - Behavior: Preferences persist for current session only
   - Logging: Error logged with user email and exception

3. **First-time user (no preferences record):**
   - User sees: Chat starts with default mode/context
   - Behavior: Normal - defaults applied
   - Logging: Info log "New user, using defaults"

4. **Invalid mode/context values in database:**
   - User sees: Fallback to defaults
   - Behavior: Validate mode in const.MODES, context in context_list
   - Logging: Warning logged with invalid values

**User-Facing Error Messages:**
- None - all errors handled silently with graceful degradation
- Users always get working chat (defaults or saved preferences)

**Logging Requirements:**
- Info: Successful preference load/save with user email, mode, context
- Warning: Invalid preference values from database
- Error: Database exceptions with user email and error details

**Recovery Procedures:**
- All failures fall back to session state or defaults
- No user intervention required
- Database issues don't block chat functionality

## Testing Strategy

### Unit Tests

If pytest suite is implemented:

```python
def test_get_preferences_existing_user():
    # Setup: Create user_preferences record
    # Execute: get_preferences(db, email)
    # Assert: Returns correct UserPreferencesModel

def test_get_preferences_new_user():
    # Execute: get_preferences(db, "new@email.com")
    # Assert: Returns None

def test_save_preferences_new_user():
    # Execute: save_preferences(db, "new@email.com", "Answer", "Intro-Variables")
    # Assert: Record created in database with correct values

def test_save_preferences_existing_user():
    # Setup: Create existing record with "Tutor", "General Python"
    # Execute: save_preferences(db, email, "Answer", "Intro-Functions")
    # Assert: Record updated, not duplicated
```

### Integration Tests

Manual integration tests:

1. **Database Table Creation:**
   - Start fresh database
   - Run app
   - Verify user_preferences table created

2. **PostgreSQL CRUD:**
   - Call save_preferences(), verify row in database
   - Call get_preferences(), verify correct data returned
   - Update preferences, verify database updated

3. **Session Isolation:**
   - User A sets preferences
   - User B logs in
   - Verify User B doesn't see User A's preferences

### Manual Testing

**Test Case 1: First-Time User (New User Flow)**
1. Delete user from user_preferences table (or use new email)
2. Log in as user
3. Verify chat starts with "Tutor" mode and "General Python" context
4. Change to "Answer" mode and "Intro-Variables" context
5. Click "Save + New Chat"
6. Verify new chat session starts with selected preferences
7. Log out and log back in
8. Verify preferences persisted ("Answer", "Intro-Variables")

**Test Case 2: Returning User (Load Saved Preferences)**
1. User has saved preferences in database (e.g., "Answer", "Intro-Functions")
2. Log in as user
3. Verify chat starts with saved mode and context
4. Verify greeting message reflects correct mode and context

**Test Case 3: Reset to Defaults**
1. User has saved preferences (e.g., "Answer", "Intro-Classes")
2. Log in and verify preferences loaded
3. Click "Reset to Defaults" button
4. Verify chat resets to "Tutor" and "General Python"
5. Log out and log back in
6. Verify defaults persisted

**Test Case 4: Multiple Session Changes**
1. Log in with saved preferences
2. Change mode/context multiple times using "Save + New Chat"
3. Verify each change is saved to database
4. Log out and log back in
5. Verify latest preferences loaded

**Test Case 5: Database Connection Failure (Error Scenario)**
1. Stop PostgreSQL database
2. Attempt to log in
3. Verify app falls back to defaults gracefully
4. Verify chat still functional with defaults
5. Check logs for error message

**Test Case 6: Admin vs Non-Admin User**
1. Log in as admin user, set preferences
2. Log out, log in as roster user, set different preferences
3. Log out, log in as admin again
4. Verify each user's preferences independent and correct

**Edge Cases:**
- Empty email string (shouldn't happen, but validate)
- Invalid mode value in database (validate and fallback)
- Invalid context value in database (validate and fallback)
- Database table doesn't exist (should auto-create)
- Concurrent login sessions (same user, different tabs) - preferences should sync on next login

## Rollback Plan

**How to Revert:**

1. **Code Rollback:**
   - Remove import of `get_preferences` and `save_preferences` from appnew.py
   - Remove preference loading code after authentication
   - Remove preference saving code in button handlers
   - Remove `from dal.models import UserPreferencesModel` from db.py
   - Delete `/workspaces/ist256-chatapp/app/dal/user_preferences.py`
   - Revert VERSION constant in constants.py

2. **Database Rollback:**
   - User preferences table can remain (benign, won't affect app)
   - Optional: DROP TABLE user_preferences; (if cleanup desired)

3. **Verification:**
   - App should start with default "Tutor" and "General Python" for all users
   - No database errors related to user_preferences

**Rollback Trigger Conditions:**
- Critical database performance issues
- Data corruption in user_preferences table
- Unexpected behavior with preference loading

**Rollback Impact:**
- Users lose saved preferences
- All users start with defaults on next login
- No data loss in logs or other tables

## References

- Related issues: N/A
- Related PRs: N/A
- External docs:
  - SQLModel documentation: https://sqlmodel.tiangolo.com/
  - Streamlit session state: https://docs.streamlit.io/library/api-reference/session-state

---

**Generated**: 2025-12-27
**Author**: AI-assisted design via /design command
**Version**: v1.0.10
