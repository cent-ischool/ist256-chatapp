# Technical Specification: Admin Menu Integration - v1.0.7

## Overview

Version 1.0.7 adds an admin-only menu to the sidebar of appnew.py that provides access to existing administrative pages: Settings, Prompts, and Session debug. This feature reuses the existing admin page implementations from app.py without modifications, creating a streamlined admin experience within the new UI architecture.

**Key Features:**
- Admin menu expander in sidebar (visible only to admin users)
- Page routing for Chat, Settings, Prompts, and Session pages
- Conditional display based on user validation level
- Zero modifications to existing admin page implementations
- Seamless integration with existing authentication/authorization

## Architecture Changes

### Components Affected

- `/workspaces/ist256-chatapp/app/chat/appnew.py`
  - **Lines**: After line 115 (after version display in sidebar)
  - **Changes**: Add admin menu expander with page selection radio buttons
  - **Changes**: Add page routing logic to display selected admin page
  - **Changes**: Wrap main chat interface in conditional (only show if page == "Chat")

### New Components

None. This version reuses existing components:
- `/workspaces/ist256-chatapp/app/chat/settings.py` (existing, no changes)
- `/workspaces/ist256-chatapp/app/chat/prompts.py` (existing, no changes)
- `/workspaces/ist256-chatapp/app/chat/session.py` (existing, no changes)

### Dependencies

**Internal Dependencies:**
- v1.0.2 (authentication and authorization for admin user detection)
- Existing admin pages: settings.py, prompts.py, session.py

**External Libraries:**
- No new dependencies required
- Uses existing Streamlit components: `st.expander()`, `st.radio()`

## Data Models

### Database Changes

None. This is a UI-only feature.

### API Changes

None. No new functions or endpoints.

## Technical Design

### Backend Implementation

No backend changes required. This feature only affects UI routing logic in appnew.py.

**Data Flow:**
1. User authentication completes (v1.0.2)
2. User validation determines user type: "admin", "exception", or "roster"
3. If user type == "admin", admin menu expander is rendered in sidebar
4. User selects page from radio buttons
5. Page selection stored in `st.session_state.admin_page`
6. Routing logic displays appropriate page function or main chat interface

### Frontend Implementation

**UI Changes:**

1. **Admin Menu in Sidebar** (after line 115 in appnew.py):
   ```python
   if st.session_state.validated == "admin":
       with st.expander("👔 Admin Menu", expanded=False):
           admin_page = st.radio(
               "Navigate to:",
               options=["Chat", "Settings", "Prompts", "Session"],
               index=0,
               help="Administrative pages for managing the chat application"
           )
           st.session_state.admin_page = admin_page
   ```

2. **Page Routing Logic** (before chat interface, around line 257):
   ```python
   # Determine which page to display
   current_page = st.session_state.get("admin_page", "Chat")

   if current_page == "Settings":
       from settings import show_settings
       show_settings()
   elif current_page == "Prompts":
       from prompts import show_prompts
       show_prompts()
   elif current_page == "Session":
       from session import show_session
       show_session()
   else:  # Chat (default)
       # [Existing chat interface code continues here]
   ```

3. **Main Chat Interface Wrapper**:
   - Wrap lines 257-368 (entire chat interface) in the else block of page routing
   - No changes to chat interface logic itself

**User Interaction Flow:**
1. Admin user logs in and is authenticated
2. Admin menu expander appears in sidebar
3. Admin clicks expander and selects a page
4. Page selection triggers rerun
5. Selected admin page is displayed
6. Admin can return to "Chat" to resume normal chat interface

**Component Hierarchy:**
```
appnew.py (main)
├── Sidebar
│   ├── Title and Version
│   └── Admin Menu (if admin user)
│       └── Page Selection Radio
└── Main Area
    ├── Settings Page (if selected)
    ├── Prompts Page (if selected)
    ├── Session Page (if selected)
    └── Chat Interface (default)
```

### Integration Points

**Authentication/Authorization:**
- Admin menu only visible when `st.session_state.validated == "admin"`
- Admin user detection established in v1.0.2 (lines 147-149 in appnew.py)
- No additional authorization checks needed

**Session State:**
- New session variable: `st.session_state.admin_page` (default: "Chat")
- Persists across reruns to maintain page selection
- Cleared when user logs out (handled by existing session.clear())

**S3 Integration:**
- Settings and Prompts pages interact with MinIO S3 via existing `st.session_state.s3_client`
- No new S3 integration required

**Database Integration:**
- No direct database interaction in routing logic
- Admin pages use existing database connections if needed

**LLM Integration:**
- No LLM interaction in admin pages
- Chat page continues to use existing LLM integration

## Configuration

### Environment Variables

No new environment variables required. Uses existing:
- `ADMIN_USERS` (already used in v1.0.2 for admin detection)
- All S3 environment variables (used by settings.py and prompts.py)

### Config Files

**constants.py:**
- No new constants required
- VERSION already updated to "1.0.7" by /design command

**config.yaml:**
- No changes

**prompts.yaml:**
- No changes

## Security Considerations

**Authentication Requirements:**
- Admin menu only visible to authenticated users (MSAL authentication required)
- Authentication handled by v1.0.2 implementation

**Authorization/Access Control:**
- Admin menu visibility controlled by `st.session_state.validated == "admin"`
- Admin user list managed via `ADMIN_USERS` environment variable
- Non-admin users cannot access admin pages (menu not displayed)

**Data Privacy:**
- Session debug page displays all session variables (admin-only, acceptable risk)
- Settings and Prompts pages allow modification of sensitive configuration (admin-only, intended behavior)

**Input Validation:**
- Page selection limited to predefined options via `st.radio()` (no arbitrary input)
- Settings and Prompts pages have existing validation (unchanged)

**SQL Injection Prevention:**
- No new database queries introduced
- Existing queries use parameterized statements via SQLModel

**XSS Prevention:**
- No new user-generated content rendered
- Streamlit handles XSS prevention automatically

## Performance Considerations

**Scalability:**
- Minimal impact: adds one conditional check and one radio button per page load
- Page routing uses simple if/elif/else (O(1) complexity)
- No additional database queries or API calls

**Caching:**
- No caching required for page routing logic
- Admin pages use existing S3 caching (unchanged)

**Database Queries:**
- No new queries introduced
- Session page reads from session state (in-memory, no DB call)

**Memory Usage:**
- One additional session variable: `admin_page` (string, negligible memory)
- Admin pages use existing session state and S3 clients (no duplication)

## Error Handling

### Expected Errors

1. **Admin page import failure:**
   - **Scenario**: settings.py, prompts.py, or session.py missing
   - **Handling**: Wrap imports in try/except, display st.error()
   - **User Message**: "Unable to load admin page. Please contact support."
   - **Logging**: `logger.error(f"Failed to import admin page: {page_name}")`

2. **Invalid page selection:**
   - **Scenario**: Session state corruption or manual manipulation
   - **Handling**: Default to "Chat" page
   - **User Message**: None (silent fallback)
   - **Logging**: `logger.warning(f"Invalid page selection: {current_page}, defaulting to Chat")`

3. **S3 connection failure in admin pages:**
   - **Scenario**: Settings/Prompts pages cannot reach S3
   - **Handling**: Existing error handling in settings.py and prompts.py (unchanged)
   - **User Message**: Handled by existing pages
   - **Logging**: Existing logging in admin pages

### Logging Requirements

- Log page navigation for admin users:
  ```python
  logger.info(f"Admin user {st.session_state.auth_model.email} navigated to {current_page}")
  ```
- Log admin menu access:
  ```python
  logger.debug(f"Admin menu displayed for {st.session_state.auth_model.email}")
  ```

## Testing Strategy

### Unit Tests

No unit tests required (UI-only feature, no isolated functions to test).

### Integration Tests

1. **Test admin menu visibility:**
   - Login as admin user → verify admin menu appears
   - Login as roster user → verify admin menu does not appear
   - Login as exception user → verify admin menu does not appear

2. **Test page routing:**
   - Select "Settings" → verify Settings page displays
   - Select "Prompts" → verify Prompts page displays
   - Select "Session" → verify Session page displays
   - Select "Chat" → verify main chat interface displays

3. **Test admin page functionality:**
   - Settings page: modify config, save, verify persistence
   - Prompts page: edit prompt, save, verify persistence
   - Session page: verify session variables display

### Manual Testing

**Admin User Test Cases:**
- [ ] Login as admin user (email in ADMIN_USERS)
- [ ] Verify admin menu expander appears in sidebar
- [ ] Click expander, verify radio buttons display
- [ ] Select "Settings", verify settings page loads
- [ ] Modify a setting, save, verify saved to S3
- [ ] Select "Prompts", verify prompts page loads
- [ ] Edit a prompt, save, verify saved to S3
- [ ] Select "Session", verify session debug page loads
- [ ] Verify session variables display correctly
- [ ] Select "Chat", verify return to main chat interface
- [ ] Verify chat history persists after navigating away
- [ ] Verify context and mode selections persist

**Non-Admin User Test Cases:**
- [ ] Login as roster user (email in roster, not admin)
- [ ] Verify admin menu does NOT appear
- [ ] Verify chat interface works normally
- [ ] Login as exception user (email in ROSTER_EXCEPTION_USERS)
- [ ] Verify admin menu does NOT appear
- [ ] Verify chat interface works normally

**Edge Cases:**
- [ ] Admin user changes mode/context, navigates to Settings, returns to Chat → verify mode/context preserved
- [ ] Admin user starts chat, navigates away, returns → verify chat history preserved
- [ ] Admin user modifies settings, does not restart → verify old settings still in use until restart
- [ ] Empty admin_page session variable → verify defaults to "Chat"
- [ ] Invalid page name in session state → verify graceful fallback

## Rollback Plan

1. **Identify rollback need:**
   - Admin pages not loading
   - Page routing broken
   - Chat interface inaccessible

2. **Rollback procedure:**
   - Revert changes to appnew.py (restore from git history)
   - Commit rollback: `git revert <commit-hash>`
   - Push to remote and redeploy

3. **Verification:**
   - Login as admin user, verify chat interface works
   - Login as non-admin user, verify chat interface works
   - Verify no error messages in logs

4. **No database migration rollback needed** (no schema changes)

5. **No configuration rollback needed** (no config changes)

## References

- Related versions: v1.0.2 (authentication/authorization dependency)
- Related files:
  - [appnew.py](../../app/chat/appnew.py) - Main modification target
  - [settings.py](../../app/chat/settings.py) - Existing admin page
  - [prompts.py](../../app/chat/prompts.py) - Existing admin page
  - [session.py](../../app/chat/session.py) - Existing admin page
- CLAUDE.md: Admin features section (lines 257-267)

---

**Generated**: 2025-12-27
**Author**: AI-assisted design via /design command
**Version**: 1.0.7
