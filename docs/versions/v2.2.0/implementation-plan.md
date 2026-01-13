# Implementation Plan: Roster Management & Session Enhancement - v2.2.0

## Timeline

- **Estimated effort**: 3-5 hours
- **Complexity**: Medium
- **Dependencies**: v2.1.0 must be complete

## Phase 1: Preparation

### Tasks

- [ ] Review technical specification ([docs/versions/v2.2.0/technical-spec.md](technical-spec.md))
- [ ] Set up development branch: `feature/v2.2.0-roster-management`
- [ ] Verify S3 access and current roster file location
- [ ] Review existing admin pages (settings.py, export.py) for patterns
- [ ] Verify admin user credentials for testing

### Prerequisites

- v2.1.0 complete and deployed
- S3 access configured and working
- Roster file exists in S3 (or can be created)
- Admin credentials available for testing

## Phase 2: Backend Implementation - S3Client Enhancement

### Tasks

- [ ] Add `put_roster()` method to S3Client class
- [ ] Test method with sample email list
- [ ] Verify format matches `get_roster()` expectations

### Files to Modify

- `/workspaces/ist256-chatapp/app/dal/s3.py`
  - **Changes**: Add `put_roster()` method after line 95
  - **Lines**: ~95-115 (new method)
  - **Reason**: Enable saving roster from web UI to S3

### Implementation Detail

Add after `list_objects()` method (line 95):

```python
def put_roster(self, bucket_name: str, object_key: str, emails: List[str]) -> None:
    """
    Upload roster file (comma-separated emails) to S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (roster file name)
        emails: List of email addresses

    Returns:
        None
    """
    # Join emails with commas (matching format of get_roster)
    content = ",".join(emails)

    # Use existing put_text_file method
    self.put_text_file(bucket_name, object_key, content)
    logger.info(f"Uploaded roster to s3://{bucket_name}/{object_key}, email_count={len(emails)}")
```

### Testing

```python
# Quick test in s3.py if __name__ == "__main__" block
test_emails = ["user1@syr.edu", "user2@syr.edu", "user3@syr.edu"]
s3client.put_roster(os.environ["S3_BUCKET"], "test-roster.txt", test_emails)
retrieved = s3client.get_text_file(os.environ["S3_BUCKET"], "test-roster.txt")
print(f"Saved and retrieved: {retrieved}")
# Should print: "user1@syr.edu,user2@syr.edu,user3@syr.edu"
```

## Phase 3: Frontend Implementation - Roster Page

### Tasks

- [ ] Create new file: `/workspaces/ist256-chatapp/app/chat/roster.py`
- [ ] Implement `show_roster()` function
- [ ] Add roster loading logic
- [ ] Add text area for editing
- [ ] Implement save logic with validation
- [ ] Add error handling and user feedback
- [ ] Test with admin user

### Files to Create

- `/workspaces/ist256-chatapp/app/chat/roster.py`
  - **Purpose**: Admin page for roster/whitelist management
  - **Key functions**:
    - `show_roster()` - Main page rendering function
  - **UI Components**:
    - `st.title()` - Page title
    - `st.metric()` - Email count display
    - `st.text_area()` - Roster editor (300px height)
    - `st.button()` - Save and Reset buttons
    - `st.success()` / `st.error()` - Feedback messages

### Implementation Structure

```python
import os
import streamlit as st
from loguru import logger
from dal.s3 import S3Client


def show_roster():
    """Render the Roster management page in Streamlit."""

    # Initialize S3 client
    s3client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )

    st.title("Roster Management")
    st.markdown("Manage the whitelist of authorized users (roster).")

    # Load current roster from S3
    try:
        current_roster_text = s3client.get_text_file(
            os.environ["S3_BUCKET"],
            os.environ["ROSTER_FILE"]
        )
        emails = [email.strip() for email in current_roster_text.split(",") if email.strip()]
        logger.info(f"Loaded roster from S3: {len(emails)} emails")
    except Exception as e:
        st.error(f"Failed to load roster from S3: {e}")
        logger.error(f"Failed to load roster: {e}")
        emails = []
        current_roster_text = ""

    # Display stats
    st.metric("Total Emails in Roster", len(emails))

    # Editable text area
    st.header("Edit Roster")
    st.markdown("""
    **Instructions:**
    - Enter one email per line or comma-separated
    - Emails will be normalized (trimmed, lowercased) on save
    - Empty lines will be ignored
    """)

    roster_input = st.text_area(
        "Roster Emails",
        value="\n".join(emails),  # Display one per line
        height=300,
        help="List of authorized email addresses, one per line"
    )

    # Save and Reset buttons
    col1, col2 = st.columns([1, 3])
    with col1:
        save_button = st.button("💾 Save Roster", type="primary")
    with col2:
        if st.button("🔄 Reset to Current"):
            st.rerun()

    if save_button:
        try:
            # Parse input (handle both newline and comma separated)
            input_text = roster_input.replace("\n", ",")
            new_emails = [email.strip().lower() for email in input_text.split(",") if email.strip()]

            # Remove duplicates while preserving order
            seen = set()
            unique_emails = []
            for email in new_emails:
                if email not in seen:
                    seen.add(email)
                    unique_emails.append(email)

            # Validate emails (basic check)
            invalid_emails = [e for e in unique_emails if "@" not in e or "." not in e]
            if invalid_emails:
                st.warning(f"Warning: {len(invalid_emails)} potentially invalid emails detected")
                with st.expander("Show invalid emails"):
                    st.write(invalid_emails)

            # Save to S3
            s3client.put_roster(
                os.environ["S3_BUCKET"],
                os.environ["ROSTER_FILE"],
                unique_emails
            )

            st.success(f"✅ Roster saved successfully! Total emails: {len(unique_emails)}")
            logger.info(f"Admin {st.session_state.auth_model.email} saved roster with {len(unique_emails)} emails")

            # Show diff if changed
            if len(unique_emails) != len(emails):
                st.info(f"Email count changed: {len(emails)} → {len(unique_emails)}")

        except Exception as e:
            st.error(f"Failed to save roster: {e}")
            logger.error(f"Failed to save roster: {e}", exc_info=True)
```

## Phase 4: Frontend Implementation - Session Page Enhancement

### Tasks

- [ ] Update `/workspaces/ist256-chatapp/app/chat/session.py`
- [ ] Add permission sections (Admin, Exception, Roster)
- [ ] Load permission lists from environment and S3
- [ ] Display current user's permission level
- [ ] Add authorization logic reference
- [ ] Preserve existing session state display

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/session.py`
  - **Changes**: Complete rewrite to add permission display
  - **Lines**: 1-8 (expand significantly)
  - **Reason**: Provide visibility into authorization system

### Implementation

```python
import os
import streamlit as st
from dal.s3 import get_roster


def show_session():
    """Display session variables and user permission information."""
    st.title("Session Debug & User Permissions")

    # Permission Information Section
    st.header("👥 User Permissions")

    # Load permission lists
    admin_users = [user.lower().strip() for user in os.environ.get("ADMIN_USERS", "").split(",") if user.strip()]
    exception_users = [user.lower().strip() for user in os.environ.get("ROSTER_EXCEPTION_USERS", "").split(",") if user.strip()]

    try:
        roster_users = [user.lower().strip() for user in get_roster(
            os.environ["S3_HOST"],
            os.environ["S3_ACCESS_KEY"],
            os.environ["S3_SECRET_KEY"],
            os.environ["S3_BUCKET"],
            os.environ["ROSTER_FILE"]
        ) if user.strip()]
    except Exception as e:
        st.error(f"Failed to load roster: {e}")
        roster_users = []

    # Display current user's permission level
    if 'auth_model' in st.session_state:
        current_email = st.session_state.auth_model.email
        if 'validated' in st.session_state:
            user_type = st.session_state.validated
            st.success(f"Current User: **{current_email}** (Permission: **{user_type}**)")

    # Admin Users Section
    with st.expander(f"🔐 Admin Users ({len(admin_users)})", expanded=True):
        st.markdown("**Source:** `ADMIN_USERS` environment variable")
        st.markdown("**Access:** Full admin access (Settings, Export, Roster, Session pages)")
        if admin_users:
            for email in admin_users:
                st.text(f"• {email}")
        else:
            st.info("No admin users configured")

    # Exception Users Section
    with st.expander(f"⚡ Exception Users ({len(exception_users)})", expanded=False):
        st.markdown("**Source:** `ROSTER_EXCEPTION_USERS` environment variable")
        st.markdown("**Access:** Bypass roster check, chat access only (no admin pages)")
        if exception_users:
            for email in exception_users:
                st.text(f"• {email}")
        else:
            st.info("No exception users configured")

    # Roster Users Section
    with st.expander(f"📋 Roster Users ({len(roster_users)})", expanded=False):
        st.markdown(f"**Source:** `{os.environ.get('ROSTER_FILE', 'roster.txt')}` in MinIO S3")
        st.markdown("**Access:** Standard chat access (no admin pages)")
        if roster_users:
            # Show first 50, with option to see all
            display_count = 50
            for email in roster_users[:display_count]:
                st.text(f"• {email}")
            if len(roster_users) > display_count:
                if st.button(f"Show all {len(roster_users)} emails"):
                    for email in roster_users[display_count:]:
                        st.text(f"• {email}")
        else:
            st.info("No roster users found (empty roster)")

    # Authorization Logic Reference
    with st.expander("ℹ️ Authorization Logic", expanded=False):
        st.markdown("""
        **User authentication and authorization follows this order:**

        1. User logs in via Azure AD (MSAL)
        2. Email extracted from authentication token
        3. Authorization check (in order):
           - If email in **Admin Users** → Grant admin access
           - Else if email in **Exception Users** → Grant chat access
           - Else if email in **Roster Users** → Grant chat access
           - Else → **Deny access** (show unauthorized message)

        **Note:** Admin users have full access including admin pages. Exception and Roster users have chat access only.
        """)

    # Session State Section
    st.header("🔍 Session State Variables")
    st.markdown("**Current Streamlit session state:**")
    st.json({k: str(v) for k, v in st.session_state.items()})
```

## Phase 5: Admin Menu & Page Routing

### Tasks

- [ ] Update admin menu options in app.py
- [ ] Add page routing for Roster page
- [ ] Test navigation to all admin pages

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/app.py`
  - **Changes**: Add "Roster" to admin menu and routing
  - **Lines to modify**:
    - Line 162: Update menu options
    - After line 323: Add Roster page routing
  - **Reason**: Make Roster page accessible from admin menu

### Admin Menu Update (Line 162)

```python
# Before:
options=["Chat", "Settings", "Export", "Session"]

# After:
options=["Chat", "Settings", "Export", "Roster", "Session"]
```

### Page Routing (After line 323, before Session routing)

```python
elif current_page == "Roster":
    try:
        import roster
        roster.show_roster()
        logger.info(f"Admin user {st.session_state.auth_model.email} navigated to Roster")
    except Exception as e:
        st.error("Unable to load Roster page. Try refreshing your browser. If the problem persists, contact mafudge@syr.edu.")
        logger.error(f"Failed to load Roster page: user={st.session_state.auth_model.email}, error={e}", exc_info=True)
```

## Phase 6: Configuration & Constants

### Tasks

- [ ] Update VERSION = "2.2.0" in constants.py
- [ ] No other configuration changes needed

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/constants.py`
  - **Changes**: Update VERSION constant on line 1
  - **Before**: `VERSION="2.1.0"`
  - **After**: `VERSION="2.2.0"`

## Phase 7: Testing

### Manual Testing Checklist

#### S3Client Testing
- [ ] Test `put_roster()` method with sample emails
- [ ] Verify saved roster can be retrieved with `get_roster()`
- [ ] Test with empty list
- [ ] Test with very long list (1000+ emails)

#### Roster Page Testing
- [ ] **Access Control**
  - [ ] Admin user can access Roster page
  - [ ] Non-admin user cannot access Roster page
  - [ ] Direct URL navigation blocked for non-admin

- [ ] **Load Functionality**
  - [ ] Current roster loads correctly
  - [ ] Email count metric displays
  - [ ] Emails display one per line in text area
  - [ ] Empty roster handled gracefully

- [ ] **Edit Functionality**
  - [ ] Can add new emails
  - [ ] Can remove emails
  - [ ] Can edit existing emails
  - [ ] Accepts newline-separated format
  - [ ] Accepts comma-separated format
  - [ ] Accepts mixed format

- [ ] **Save Functionality**
  - [ ] Save button works
  - [ ] Success message appears
  - [ ] Saved roster persists in S3
  - [ ] Page reload shows saved changes
  - [ ] Email normalization works (lowercase, trim)
  - [ ] Duplicate removal works
  - [ ] Invalid email warning appears

- [ ] **UI Elements**
  - [ ] Reset button reloads original roster
  - [ ] Invalid email expander shows bad emails
  - [ ] Email count change notification shows
  - [ ] Error messages display for S3 failures

#### Session Page Testing
- [ ] **Permission Display**
  - [ ] Current user's permission shown
  - [ ] Admin Users section displays correctly
  - [ ] Exception Users section displays correctly
  - [ ] Roster Users section displays correctly
  - [ ] Email counts are accurate

- [ ] **Expanders**
  - [ ] Admin section expanded by default
  - [ ] Exception section collapsed by default
  - [ ] Roster section collapsed by default
  - [ ] All expanders toggle correctly

- [ ] **Large Roster Handling**
  - [ ] First 50 roster emails show
  - [ ] "Show all" button appears if >50
  - [ ] "Show all" button displays remaining emails

- [ ] **Session State**
  - [ ] Session state variables still display
  - [ ] JSON format is readable

#### Admin Menu Testing
- [ ] "Roster" option appears in admin menu
- [ ] "Roster" positioned between "Export" and "Session"
- [ ] Clicking "Roster" navigates to roster page
- [ ] Other admin pages still accessible
- [ ] Non-admin users don't see "Roster" option

#### Integration Testing
- [ ] Save roster → logout → login → verify roster saved
- [ ] Add user to roster → user can login
- [ ] Remove user from roster → user cannot login (on next session)
- [ ] Roster changes reflected in Session page
- [ ] Multiple admins can edit roster (no conflicts)

#### Edge Cases
- [ ] Empty roster file
- [ ] Roster file missing from S3 (error handling)
- [ ] S3 unavailable (error handling)
- [ ] Very large roster (1000+ emails)
- [ ] Roster with malformed emails
- [ ] Roster with spaces, mixed case, duplicates
- [ ] Save with network timeout
- [ ] Concurrent edits by multiple admins

#### Error Scenarios
- [ ] S3 connection failure displays error
- [ ] Invalid roster format handled
- [ ] Save failure doesn't clear form
- [ ] Error logs captured correctly

## Phase 8: Documentation

### Tasks

- [ ] Update CLAUDE.md if needed (probably not required)
- [ ] Update docs/versions/README.md with v2.2.0 entry
- [ ] Update project_requirements.md status

### Files to Update

- `/workspaces/ist256-chatapp/docs/versions/README.md`
  - **Changes**: Add v2.2.0 row to version table
  - **Status**: In Development

- `/workspaces/ist256-chatapp/docs/project_requirements.md`
  - **Changes**: Update v2.2.0 status to Released (after deployment)
  - **Release Date**: TBD → actual date

- `/workspaces/ist256-chatapp/CLAUDE.md` (optional)
  - **Changes**: Mention Roster admin page in Admin Features section
  - **Section**: Admin Features (~line 250)

## Phase 9: Deployment

### Tasks

- [ ] Commit changes: "Implement v2.2.0: Roster management UI and session enhancement"
- [ ] Push feature branch to remote
- [ ] Create PR to main branch
- [ ] Code review
- [ ] Merge to main
- [ ] Verify CI/CD pipeline passes
- [ ] Monitor deployment logs
- [ ] Verify roster page works in production

### Deployment Checklist

- [ ] All manual tests passing locally
- [ ] No merge conflicts with main
- [ ] VERSION constant updated to "2.2.0"
- [ ] roster.py file created
- [ ] session.py enhanced with permissions
- [ ] Admin menu includes "Roster" option
- [ ] Page routing includes Roster page
- [ ] put_roster() method added to S3Client

### Post-Deployment

- [ ] Verify admin can access Roster page in production
- [ ] Test saving roster in production
- [ ] Verify Session page shows permissions correctly
- [ ] Monitor logs for errors
- [ ] Notify admins of new roster management feature

## Dependencies

### Internal Dependencies

- **v2.1.0** (Settings simplification) must be complete
- Admin authentication system must be functional
- S3 bucket must be accessible and writable

### External Dependencies

None - uses existing libraries (streamlit, minio, loguru)

### Blocked By

None - all prerequisites available

## Risks & Mitigation

### Risk 1: Concurrent roster edits by multiple admins

- **Impact**: Medium (one admin's changes could overwrite another's)
- **Probability**: Low (typically only one admin managing roster)
- **Mitigation**:
  - No locking mechanism (too complex for v2.2.0)
  - Document that last save wins
  - Consider adding timestamp of last edit in future version
  - Logs show all changes with timestamps for audit

### Risk 2: Invalid emails in roster break authorization

- **Impact**: Medium (users might not be able to login)
- **Probability**: Low (basic validation in place)
- **Mitigation**:
  - Basic email validation warns admin
  - `get_roster()` is tolerant of format variations
  - Admins can immediately edit and fix
  - S3 file can be manually edited as fallback

### Risk 3: Large roster causes UI performance issues

- **Impact**: Low (UI might be slow with 10,000+ emails)
- **Probability**: Very Low (typical roster <1000 emails)
- **Mitigation**:
  - `st.text_area` handles large text well
  - Session page uses expanders and pagination (first 50)
  - No performance issues expected for reasonable roster sizes

### Risk 4: S3 save fails, form data lost

- **Impact**: Low (admin needs to re-edit)
- **Probability**: Very Low (S3 is reliable)
- **Mitigation**:
  - Error handling preserves form data on failure
  - Admin can retry save immediately
  - Copy-paste from text area if needed

## Success Criteria

- [ ] Roster page accessible from admin menu
- [ ] Admin can view current roster
- [ ] Admin can edit and save roster to S3
- [ ] Session page shows permission sections
- [ ] Permission sections display correct user lists
- [ ] `put_roster()` method works correctly
- [ ] Non-admin users cannot access Roster page
- [ ] Roster changes persist across sessions
- [ ] VERSION displays "2.2.0" in UI
- [ ] No errors in production logs
- [ ] Email normalization and duplicate removal work
- [ ] Invalid email warnings appear
- [ ] All manual tests pass

## Rollback Procedure

1. **Identify issue**
   - Check logs for exceptions
   - Verify user reports

2. **Rollback code**
   - `git revert <v2.2.0-commit-hash>`
   - Deploy reverted version

3. **Roster data**
   - Roster file in S3 is unaffected by code rollback
   - If roster was corrupted, restore from S3 version history
   - Or manually re-upload correct roster file

4. **Verify rollback**
   - Admin menu no longer shows "Roster" option
   - Session page shows simple session state (no permissions)
   - Chat functionality unchanged
   - Authorization still works (roster file intact)

5. **Communication**
   - Notify admins of rollback
   - Document issue for future fix

## Post-Deployment

### Monitoring

Monitor for first 24-48 hours:
- Application error logs (loguru output)
- S3 access errors (roster read/write failures)
- Admin usage of Roster page
- User login issues (roster-related)

### Key Metrics

- No increase in error rate
- Roster page load time (<2 seconds)
- Save operations successful (100%)
- No authorization failures due to roster issues

### Follow-up Tasks

- [ ] Gather admin feedback on Roster page UX
- [ ] Consider adding roster change history (v2.3.0+)
- [ ] Consider adding bulk import/export (CSV) in future
- [ ] Update admin training documentation

---

**Generated**: 2026-01-13
**Author**: AI-assisted planning via /design command
**Version**: 2.2.0
