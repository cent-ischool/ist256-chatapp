# Implementation Plan: User Preferences Persistence - v1.0.10

## Timeline

- Estimated effort: 2-3 hours
- Complexity: Low
- Suggested sprint: Can be completed in single session

## Phase 1: Preparation

### Tasks

- [ ] Review technical specification
- [ ] Set up development branch: `feature/v1.0.10-user-preferences`
- [ ] Update TODO.txt with version tasks
- [ ] Verify PostgreSQL database is accessible
- [ ] Review existing UserPreferencesModel in models.py
- [ ] Review existing set_context() function in appnew.py
- [ ] Confirm SQLModel auto-creates tables on startup

### Prerequisites

- PostgreSQL database running and accessible via DATABASE_URL
- Existing codebase at v1.0.9 or later
- UserPreferencesModel already defined in app/dal/models.py

## Phase 2: Backend Implementation

### Tasks

- [ ] Create app/dal/user_preferences.py module
- [ ] Implement get_preferences() function with error handling
- [ ] Implement save_preferences() function with upsert logic
- [ ] Add loguru logging to both functions
- [ ] Update app/dal/db.py to import UserPreferencesModel for table creation
- [ ] Test functions independently using database session

### Files to Modify

- `/workspaces/ist256-chatapp/app/dal/db.py`
  - **Changes**: Add `from dal.models import UserPreferencesModel` to imports (line 6)
  - **Lines**: After line 6 (after `from dal.models import LogModel`)
  - **Reason**: Ensure user_preferences table is auto-created by SQLModel.metadata.create_all()

### Files to Create

- `/workspaces/ist256-chatapp/app/dal/user_preferences.py`
  - **Purpose**: Data access layer for user preferences CRUD operations
  - **Key functions**:
    - `get_preferences(db: PostgresDb, user_email: str) -> Optional[UserPreferencesModel]`
      - Query database for user preferences by email
      - Return None if not found (first-time user)
      - Handle database exceptions gracefully
      - Log retrieval operation
    - `save_preferences(db: PostgresDb, user_email: str, mode: str, context: str) -> UserPreferencesModel`
      - Check if preferences exist for user
      - If exists: update mode and context
      - If not exists: create new record
      - Commit to database
      - Return saved model
      - Handle database exceptions
      - Log save operation

**Implementation Template for user_preferences.py:**

```python
from typing import Optional
from loguru import logger
from sqlmodel import select
from dal.db import PostgresDb
from dal.models import UserPreferencesModel


def get_preferences(db: PostgresDb, user_email: str) -> Optional[UserPreferencesModel]:
    """
    Retrieve user preferences from database.

    Args:
        db: PostgresDb instance
        user_email: User's email address (primary key)

    Returns:
        UserPreferencesModel if found, None if not found or error occurs
    """
    try:
        with db.get_session() as session:
            statement = select(UserPreferencesModel).where(
                UserPreferencesModel.user_email == user_email
            )
            preferences = session.exec(statement).first()

            if preferences:
                logger.info(f"Loaded preferences: email={user_email}, mode={preferences.mode}, context={preferences.context}")
            else:
                logger.info(f"No preferences found for: email={user_email}")

            return preferences

    except Exception as e:
        logger.error(f"Error loading preferences: email={user_email}, error={e}")
        return None


def save_preferences(db: PostgresDb, user_email: str, mode: str, context: str) -> UserPreferencesModel:
    """
    Save or update user preferences in database.

    Args:
        db: PostgresDb instance
        user_email: User's email address (primary key)
        mode: AI mode ("Tutor" or "Answer")
        context: Chat context (assignment name or "General Python")

    Returns:
        Saved UserPreferencesModel

    Raises:
        Exception if database operation fails
    """
    try:
        with db.get_session() as session:
            # Check if preferences exist
            statement = select(UserPreferencesModel).where(
                UserPreferencesModel.user_email == user_email
            )
            existing = session.exec(statement).first()

            if existing:
                # Update existing preferences
                existing.mode = mode
                existing.context = context
                session.add(existing)
                session.commit()
                session.refresh(existing)
                logger.info(f"Updated preferences: email={user_email}, mode={mode}, context={context}")
                return existing
            else:
                # Create new preferences
                new_prefs = UserPreferencesModel(
                    user_email=user_email,
                    mode=mode,
                    context=context
                )
                session.add(new_prefs)
                session.commit()
                session.refresh(new_prefs)
                logger.info(f"Created preferences: email={user_email}, mode={mode}, context={context}")
                return new_prefs

    except Exception as e:
        logger.error(f"Error saving preferences: email={user_email}, mode={mode}, context={context}, error={e}")
        raise
```

## Phase 3: Frontend Implementation

### Tasks

- [ ] Add import for get_preferences and save_preferences in appnew.py
- [ ] Add preference loading after authentication (after line 263)
- [ ] Add session state flag to prevent re-loading preferences
- [ ] Update "Save + New Chat" button handler to save preferences
- [ ] Update "Reset to Defaults" button handler to save default preferences
- [ ] Add error handling for preference load/save failures
- [ ] Test full user flow: login → load prefs → change prefs → logout → login

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/appnew.py`
  - **Changes**:
    1. Import user preference functions (after line 25)
    2. Load preferences after authentication and authorization (after line 263)
    3. Save preferences in button handlers (lines 488-493)
  - **Streamlit components**: No new components, uses existing st.session_state
  - **Integration points**: set_context() function, PostgresDb in session state

**Specific Code Additions:**

**Location 1: Add import (after line 25)**
```python
from dal.user_preferences import get_preferences, save_preferences
```

**Location 2: Load preferences after authorization (after line 263, before line 267)**
```python
    # ----------------- Load User Preferences (v1.0.10) -----------------
    if 'preferences_loaded' not in st.session_state:
        email = st.session_state.auth_model.email
        try:
            prefs = get_preferences(st.session_state.db, email)
            if prefs:
                # Validate loaded preferences against available options
                valid_modes = const.MODES
                context_list_validate = ["General Python"] + st.session_state.file_cache.get_doc_list() if 'file_cache' in st.session_state else ["General Python"]

                mode = prefs.mode if prefs.mode in valid_modes else "Tutor"
                context = prefs.context if prefs.context in context_list_validate else "General Python"

                set_context(mode, context)
                logger.info(f"Loaded user preferences: email={email}, mode={mode}, context={context}")
            else:
                # First-time user, use defaults
                set_context("Tutor", "General Python")
                logger.info(f"New user, using defaults: email={email}")
        except Exception as e:
            logger.error(f"Failed to load preferences for {email}: {e}")
            set_context("Tutor", "General Python")  # Fallback to defaults

        st.session_state.preferences_loaded = True
```

**Location 3: Save preferences in button handlers (replace lines 488-493)**
```python
            if set_mode:
                # Save preferences before setting new context (v1.0.10)
                try:
                    save_preferences(st.session_state.db, st.session_state.auth_model.email, mode, context)
                    logger.info(f"Saved preferences: email={st.session_state.auth_model.email}, mode={mode}, context={context}")
                except Exception as e:
                    logger.error(f"Failed to save preferences: {e}")

                set_context(mode, context)
                st.rerun()
            elif reset_to_defaults:
                # Save default preferences (v1.0.10)
                try:
                    save_preferences(st.session_state.db, st.session_state.auth_model.email, "Tutor", "General Python")
                    logger.info(f"Reset preferences to defaults: email={st.session_state.auth_model.email}")
                except Exception as e:
                    logger.error(f"Failed to save default preferences: {e}")

                set_context("Tutor", "General Python")
                st.rerun()
```

### Files to Create

None - all frontend changes are modifications to existing appnew.py

## Phase 4: Configuration & Constants

### Tasks

- [ ] Update `app/chat/constants.py` with VERSION = "v1.0.10"
- [ ] No changes needed to config.yaml (no new configuration)
- [ ] No changes needed to prompts.yaml
- [ ] No new constants needed

### Configuration Changes

- Update VERSION constant in `/workspaces/ist256-chatapp/app/chat/constants.py` line 1:
  ```python
  VERSION = "v1.0.10"
  ```

## Phase 5: Testing

### Tasks

- [ ] Manual testing checklist
  - [ ] Test first-time user flow (no preferences in DB)
  - [ ] Test returning user flow (preferences exist in DB)
  - [ ] Test "Save + New Chat" button saves preferences
  - [ ] Test "Reset to Defaults" button saves defaults
  - [ ] Test logout and re-login restores preferences
  - [ ] Test multiple mode/context changes persist correctly
  - [ ] Test invalid preference values in DB (manual DB edit)
  - [ ] Test admin user preferences independent from roster user
  - [ ] Test roster user preferences independent from exception user
- [ ] Integration testing
  - [ ] Database: Verify user_preferences table auto-created on startup
  - [ ] Database: Verify CRUD operations work correctly
  - [ ] Database: Verify upsert logic (insert vs update)
  - [ ] Session State: Verify preferences_loaded flag prevents re-loading
  - [ ] set_context(): Verify integration with preference loading
- [ ] Error scenario testing
  - [ ] Database connection failure during load (graceful fallback)
  - [ ] Database connection failure during save (session persists)
  - [ ] Invalid mode in database (fallback to "Tutor")
  - [ ] Invalid context in database (fallback to "General Python")

### Test Data

**Database Setup for Testing:**
1. Fresh user (no record in user_preferences)
2. Existing user with "Tutor", "General Python"
3. Existing user with "Answer", "Intro-Variables"
4. Existing user with invalid mode "InvalidMode" (test validation)
5. Existing user with invalid context "NonexistentAssignment" (test validation)

**Test Users:**
- Admin user: From ADMIN_USERS env var
- Roster user: From roster file in S3
- Exception user: From ROSTER_EXCEPTION_USERS env var

## Phase 6: Documentation

### Tasks

- [ ] Update CLAUDE.md with user preferences feature documentation
- [ ] Add section to "Key Components" describing preference persistence
- [ ] Add user_preferences.py to "Important Files" list
- [ ] Update "Database Schema" section with UserPreferencesModel table
- [ ] Add note about preference loading in "Chat Flow" section
- [ ] No README.md changes needed (internal feature)

### Documentation Files

- `/workspaces/ist256-chatapp/CLAUDE.md`
  - Add to "Key Components" → "Chat Flow" section (after line 13)
  - Add to "Database Schema" section (after line 98)
  - Add to "Important Files" section

**CLAUDE.md Updates:**

**Add to Chat Flow (after line 13):**
```markdown
**User Preferences (v1.0.10+):**
1. After successful authentication, user preferences loaded from PostgreSQL
2. If preferences exist: mode and context set to saved values
3. If no preferences: defaults to "Tutor" mode and "General Python" context
4. When user clicks "Save + New Chat" or "Reset to Defaults": preferences saved to database
5. Preferences persist across sessions and browser tabs
```

**Add to Database Schema (after UserPreferencesModel description, line 67):**
```markdown
PostgreSQL table `UserPreferencesModel`:
- `user_email` - User email (primary key)
- `mode` - AI mode ("Tutor" or "Answer")
- `context` - Assignment name or "General Python"
```

**Add to Important Files:**
```markdown
- [app/dal/user_preferences.py](app/dal/user_preferences.py) - CRUD operations for user preferences
```

## Phase 7: Deployment

### Tasks

- [ ] Commit changes with message: "Implement v1.0.10: User preferences persistence"
- [ ] Push feature branch to remote
- [ ] Create PR to main branch
- [ ] Code review
- [ ] Address review feedback
- [ ] Merge to main
- [ ] Verify CI/CD pipeline passes
- [ ] Monitor deployment
- [ ] Verify in production environment
  - [ ] Check user_preferences table created
  - [ ] Test preference loading with real users
  - [ ] Monitor logs for errors

### Deployment Checklist

- [ ] All tests passing (manual test checklist completed)
- [ ] No merge conflicts
- [ ] Version number updated to v1.0.10
- [ ] Documentation complete (CLAUDE.md updated)
- [ ] Breaking changes documented (none for this version)
- [ ] Database migration verified (auto-create table works)

### Commit Message Format

```
Implement v1.0.10: User preferences persistence

Features:
- User mode and context preferences now persist across sessions
- Preferences loaded automatically on login
- Saved when user clicks "Save + New Chat" or "Reset to Defaults"
- Graceful fallback to defaults on database errors

Technical Changes:
- Created app/dal/user_preferences.py with get/save functions
- Modified app/chat/appnew.py to load/save preferences
- Updated app/dal/db.py to import UserPreferencesModel for table creation
- Updated VERSION to v1.0.10 in constants.py

Database:
- user_preferences table auto-created via SQLModel
- No manual migration required

Testing:
- Manual testing completed for all user flows
- Error scenarios tested and verified

Dependencies: v1.0.2-v1.0.9
Complexity: Low
Effort: 2-3 hours
```

## Dependencies

### Internal Dependencies

**Required versions (must be complete first):**
- v1.0.2: Authentication and authorization
- v1.0.3: Database connection and ChatLogger
- v1.0.4: LLM integration and configuration loading
- v1.0.5: Context injection and set_context() function
- v1.0.6: Chat logging
- v1.0.7: Admin menu
- v1.0.8: UI polish
- v1.0.9: Export functionality

**Code dependencies:**
- `set_context(mode, context)` function in appnew.py
- `st.session_state.db` (PostgresDb instance)
- `st.session_state.auth_model.email` (user identification)
- `st.session_state.file_cache.get_doc_list()` (available contexts)
- `const.MODES` (valid mode values)

### External Dependencies

- PostgreSQL database (already required)
- SQLModel library (already in requirements.txt)
- No new external dependencies

### Team Dependencies

None - can be completed independently

## Risks & Mitigation

### Risk 1: Database table not auto-created on startup

- **Impact**: Medium - users can't save preferences
- **Probability**: Low - SQLModel handles this automatically
- **Mitigation**:
  - Verify UserPreferencesModel imported in db.py
  - Test with fresh database before deployment
  - Add manual CREATE TABLE script as fallback

### Risk 2: Preferences loaded before file_cache initialized

- **Impact**: Medium - invalid context validation fails
- **Probability**: Low - file_cache loaded early in initialization
- **Mitigation**:
  - Move preference loading after file_cache initialization (line 290+)
  - Add validation check for file_cache existence
  - Fallback to defaults if context_list unavailable

### Risk 3: User changes preferences in multiple browser tabs simultaneously

- **Impact**: Low - last save wins, no data corruption
- **Probability**: Medium - users may have multiple tabs open
- **Mitigation**:
  - Document behavior: preferences sync on next login
  - Database primary key prevents duplicate records
  - No locking needed (preferences are user-scoped, low conflict)

### Risk 4: Database connection failure prevents app startup

- **Impact**: High - app won't start if DB required
- **Probability**: Low - existing feature, already tested
- **Mitigation**:
  - All preference operations wrapped in try/except
  - Graceful fallback to session-only defaults
  - App remains functional without preference persistence

## Success Criteria

- [ ] All tasks completed
- [ ] Version number updated to v1.0.10 in constants.py
- [ ] All manual tests passing
- [ ] Documentation updated (CLAUDE.md)
- [ ] Code reviewed and approved
- [ ] Deployed to production
- [ ] No critical bugs reported within 24 hours
- [ ] Feature functions as specified in requirements:
  - [ ] Preferences stored in database
  - [ ] Preferences loaded on login
  - [ ] Preferences saved on "Save + New Chat"
  - [ ] Preferences saved on "Reset to Defaults"
  - [ ] Preferences persist across sessions
  - [ ] Graceful error handling

## Rollback Procedure

1. **Revert code changes:**
   - `git revert <commit-hash>` or merge revert PR
   - Remove user_preferences.py file
   - Remove imports from appnew.py and db.py
   - Revert VERSION constant to v1.0.9

2. **Database cleanup (optional):**
   - user_preferences table can remain (won't affect app)
   - If cleanup desired: `DROP TABLE user_preferences;`

3. **Verification after rollback:**
   - App starts successfully
   - All users default to "Tutor" and "General Python"
   - No database errors in logs
   - Chat functionality fully working

4. **Communication:**
   - Notify users preferences will reset to defaults
   - Document reason for rollback in incident report

## Post-Deployment

### Monitoring

**What to monitor after deployment:**
- Database logs for user_preferences table creation
- Application logs for preference load/save operations
- Error logs for database connection failures
- User behavior: are preferences being used?

**Key metrics to watch:**
- Number of user_preferences records created (should match active user count)
- Preference load success rate (target: >99%)
- Preference save success rate (target: >99%)
- Error rate for preference operations (target: <1%)

**Log Queries:**
```bash
# Check preference loading
grep "Loaded user preferences" application.log | wc -l

# Check preference saves
grep "Saved preferences" application.log | wc -l

# Check errors
grep "Error loading preferences\|Error saving preferences" application.log

# Check new users
grep "New user, using defaults" application.log | wc -l
```

**Database Queries:**
```sql
-- Count total users with preferences
SELECT COUNT(*) FROM user_preferences;

-- View preference distribution
SELECT mode, context, COUNT(*)
FROM user_preferences
GROUP BY mode, context
ORDER BY COUNT(*) DESC;

-- Find users with custom preferences (not defaults)
SELECT user_email, mode, context
FROM user_preferences
WHERE mode != 'Tutor' OR context != 'General Python';
```

### Follow-up Tasks

- [ ] Monitor preference usage for 1 week
- [ ] Analyze which modes/contexts are most popular
- [ ] Consider adding preference export/import for admin users (future enhancement)
- [ ] Consider adding UI indicator showing saved vs current preferences (future enhancement)

---

**Generated**: 2025-12-27
**Author**: AI-assisted planning via /design command
**Version**: v1.0.10
