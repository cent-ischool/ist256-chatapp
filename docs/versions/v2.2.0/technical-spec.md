# Technical Specification: Roster Management & Session Info Enhancement - v2.2.0

## Overview

Version 2.2.0 adds administrative capabilities for managing the user whitelist (roster) directly from the web interface and enhances the session debug page to display user permissions. This eliminates the need to manually edit roster files in S3 and provides better visibility into the authorization system.

### Features Summary
- **Roster Management UI** - Admin page to edit whitelist directly in the app
- **Enhanced Session Page** - Display users by permission level (admin, exception, roster)
- **S3 Roster Operations** - Add `put_roster()` method to S3Client for saving roster

## Architecture Changes

### Components Affected

| File | Change Type | Description |
|------|-------------|-------------|
| [/workspaces/ist256-chatapp/app/dal/s3.py](../../app/dal/s3.py) | Modify | Add `put_roster()` method to save roster to S3 |
| [/workspaces/ist256-chatapp/app/chat/session.py](../../app/chat/session.py) | Modify | Add permission sections showing admin/exception/roster users |
| [/workspaces/ist256-chatapp/app/chat/app.py](../../app/chat/app.py) | Modify | Add "Roster" to admin menu navigation |
| [/workspaces/ist256-chatapp/app/chat/constants.py](../../app/chat/constants.py) | Modify | Update VERSION to "2.2.0" |

### New Components

| File | Purpose |
|------|---------|
| [/workspaces/ist256-chatapp/app/chat/roster.py](../../app/chat/roster.py) | New admin page for editing and saving roster/whitelist |

### Dependencies

No new external dependencies required. Uses existing:
- `streamlit` for UI components
- `minio` for S3 operations (via S3Client)
- `loguru` for logging

## Data Models

### Database Changes

**No database schema changes** - Roster data is stored in MinIO S3 as a text file, not in PostgreSQL.

### API Changes

**S3Client class** ([app/dal/s3.py](../../app/dal/s3.py)):

**New method:**
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

    Raises:
        Exception: If S3 upload fails
    """
```

**Existing method to reference:**
- `get_roster()` - Already exists (lines 98-121), returns `List[str]` of emails

## Technical Design

### Backend Implementation

#### 1. S3Client Enhancement ([app/dal/s3.py](../../app/dal/s3.py))

Add `put_roster()` method to S3Client class (after line 95):

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

**Design rationale:**
- Reuses existing `put_text_file()` method (lines 70-88)
- Matches format of existing `get_roster()` function (comma-separated)
- Simple, maintainable implementation
- Proper logging for audit trail

#### 2. Roster Admin Page ([app/chat/roster.py](../../app/chat/roster.py) - NEW FILE)

Create new admin page for roster management:

```python
import os
import streamlit as st
from loguru import logger

from dal.s3 import S3Client


def show_roster():
    """Render the Roster management page in Streamlit."""
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
        value="\n".join(emails),  # Display one per line for readability
        height=300,
        help="List of authorized email addresses, one per line"
    )

    # Save button
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

**Design rationale:**
- Similar structure to existing `settings.py` (lines 1-81)
- Uses `st.text_area` for easy editing
- One email per line for better UX (converted to comma-separated on save)
- Email validation and duplicate removal
- Clear success/error feedback
- Audit logging for all changes

#### 3. Session Page Enhancement ([app/chat/session.py](../../app/chat/session.py))

Update to show permission-based user sections:

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

**Design rationale:**
- Provides visibility into authorization system
- Shows all three permission levels clearly
- Current user's permission highlighted
- Expandable sections for better UX
- Reference documentation for authorization logic
- Preserves existing session state display functionality

### Frontend Implementation

#### Admin Menu Update ([app/chat/app.py](../../app/chat/app.py))

Update admin menu navigation (line 162):

```python
# Before:
options=["Chat", "Settings", "Export", "Session"]

# After:
options=["Chat", "Settings", "Export", "Roster", "Session"]
```

#### Page Routing ([app/chat/app.py](../../app/chat/app.py))

Add routing for Roster page (after line 323, before Session routing):

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

### Integration Points

| Component | Integration |
|-----------|-------------|
| **MinIO S3** | Roster read via `get_roster()`, write via new `put_roster()` method |
| **PostgreSQL** | No integration - roster is S3-based |
| **Authentication** | Roster page admin-only (existing auth check applies) |
| **Session State** | Uses `st.session_state.auth_model` for current user info |
| **Environment Vars** | Reads `ADMIN_USERS`, `ROSTER_EXCEPTION_USERS`, `ROSTER_FILE`, S3 credentials |

## Configuration

### Environment Variables

**No new environment variables required.** Existing variables used:
- `S3_HOST` - MinIO server address
- `S3_BUCKET` - Bucket containing roster file
- `S3_ACCESS_KEY` - MinIO access key
- `S3_SECRET_KEY` - MinIO secret key
- `ROSTER_FILE` - Roster filename in S3 (e.g., "ist256-fall2025-roster.txt")
- `ADMIN_USERS` - Comma-separated admin emails
- `ROSTER_EXCEPTION_USERS` - Comma-separated exception emails

### Config Files

**No config file changes** - VERSION constant updated in constants.py:
```python
VERSION="2.2.0"
```

## Security Considerations

| Consideration | Handling |
|---------------|----------|
| **Admin-only access** | Roster page restricted to admin users (same check as Settings page) |
| **Input validation** | Email format validation (basic @ and . check) |
| **Authorization exposure** | Session page shows permission lists (admin-only, acceptable for debugging) |
| **Audit trail** | All roster changes logged with admin email and timestamp |
| **S3 credentials** | Never exposed in UI, loaded from environment |
| **XSS prevention** | Streamlit handles escaping, emails are text-only |
| **Injection attacks** | No SQL involved; S3 operations use parameterized methods |

**Security notes:**
- Roster page is admin-only (validated=="admin" check)
- Email validation prevents obviously invalid entries
- All roster modifications logged for audit purposes
- No sensitive data exposed to non-admin users

## Performance Considerations

| Aspect | Impact |
|--------|--------|
| **S3 operations** | One extra read for roster page load, one write on save |
| **Memory** | Roster held in memory temporarily during edit (typically <1000 emails = <50KB) |
| **UI responsiveness** | `st.text_area` handles large rosters efficiently |
| **Session page** | Permission lists loaded on demand (expandable sections) |

**Optimizations:**
- Roster loaded once per page view (not on every interaction)
- Session page uses expanders to defer rendering of large lists
- Duplicate removal and normalization done server-side (efficient)

## Error Handling

### Expected Errors

| Error | Handling | User Message |
|-------|----------|--------------|
| **S3 unavailable** | Catch exception, show error | "Failed to load roster from S3: {error}" |
| **Invalid roster format** | Parse with error tolerance | "Warning: X potentially invalid emails detected" |
| **Empty roster file** | Handle gracefully | "No roster users found (empty roster)" |
| **Save failure** | Catch exception, don't clear form | "Failed to save roster: {error}" |
| **Permission denied** | Should not occur (admin-only) | Standard unauthorized message |

### Logging

All roster operations logged with:
- Admin user email performing action
- Number of emails in roster
- Success/failure status
- Full exception traces on errors

Example log entries:
```
INFO: Admin user@syr.edu saved roster with 247 emails
ERROR: Failed to save roster: Connection timeout to S3
INFO: Loaded roster from S3: 247 emails
```

## Testing Strategy

### Unit Tests

| Test Case | Description |
|-----------|-------------|
| `test_put_roster_valid` | S3Client.put_roster() with valid email list |
| `test_put_roster_empty` | put_roster() with empty list |
| `test_roster_normalization` | Duplicate removal and lowercasing |
| `test_email_validation` | Basic email format validation |

### Integration Tests

| Test Case | Description |
|-----------|-------------|
| **Roster page load** | Admin can access and view current roster |
| **Roster save** | Edited roster persists to S3 |
| **Session page permissions** | Correctly displays admin/exception/roster lists |
| **Non-admin access** | Non-admin cannot access Roster page |

### Manual Testing Checklist

#### Roster Page Testing
- [ ] Admin can access Roster page from admin menu
- [ ] Current roster loads and displays
- [ ] Email count metric shows correct number
- [ ] Text area is editable
- [ ] Can add new emails (one per line)
- [ ] Can remove emails
- [ ] Save button works
- [ ] Success message appears after save
- [ ] Roster persists after page reload
- [ ] Invalid email warning appears for bad emails
- [ ] Duplicate emails are removed
- [ ] Emails are normalized (lowercased, trimmed)
- [ ] Reset button reloads original roster

#### Session Page Testing
- [ ] Admin can access Session page
- [ ] "User Permissions" section visible
- [ ] Current user's permission level displayed
- [ ] Admin Users section shows correct count and emails
- [ ] Exception Users section shows correct count and emails
- [ ] Roster Users section shows correct count and emails
- [ ] Expanders work correctly
- [ ] "Show all" button works for large rosters (>50)
- [ ] Authorization Logic reference section explains system
- [ ] Session State section still displays variables

#### Admin Menu Testing
- [ ] "Roster" option appears in admin menu (between Export and Session)
- [ ] Clicking "Roster" navigates to roster page
- [ ] Other admin pages still accessible

#### Authorization Testing
- [ ] Non-admin user cannot see "Roster" in menu
- [ ] Non-admin user cannot navigate to Roster page manually
- [ ] Exception user cannot access Roster page
- [ ] Roster user cannot access Roster page

#### Edge Cases
- [ ] Empty roster file (no emails)
- [ ] Very large roster (1000+ emails)
- [ ] Roster file missing from S3 (error handling)
- [ ] S3 unavailable (error handling)
- [ ] Malformed emails in roster
- [ ] Emails with spaces, uppercase, etc. (normalization)

## Rollback Plan

1. **Revert code changes**
   - `git revert <v2.2.0-commit-hash>`
   - Roster file in S3 remains unchanged (not affected by code rollback)

2. **No database rollback needed**
   - No schema changes made

3. **S3 roster file**
   - Roster changes made via UI are permanent in S3
   - If needed, restore from S3 version history
   - Or manually re-upload previous roster file

4. **Verification after rollback**
   - Admin menu shows: Chat, Settings, Export, Session (no Roster)
   - Session page shows simple session state (no permission sections)
   - Chat functionality unchanged

## References

- Requirements: [/workspaces/ist256-chatapp/docs/project_requirements.md](../../docs/project_requirements.md) (v2.2.0 section)
- S3Client: [/workspaces/ist256-chatapp/app/dal/s3.py](../../app/dal/s3.py)
- Settings page (similar pattern): [/workspaces/ist256-chatapp/app/chat/settings.py](../../app/chat/settings.py)
- Session page (current): [/workspaces/ist256-chatapp/app/chat/session.py](../../app/chat/session.py)
- Main app: [/workspaces/ist256-chatapp/app/chat/app.py](../../app/chat/app.py)

---

**Generated**: 2026-01-13
**Author**: AI-assisted design via /design command
**Version**: 2.2.0
