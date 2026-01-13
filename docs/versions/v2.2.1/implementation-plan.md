# Implementation Plan: Whitelist Refactoring & Bug Fixes - v2.2.1

## Timeline

- **Estimated effort**: 3-5 hours
- **Complexity**: Medium
- **Dependencies**: v2.2.0 must be complete

## Phase 1: Preparation

### Tasks

- [ ] Review technical specification ([docs/versions/v2.2.1/technical-spec.md](technical-spec.md))
- [ ] Set up development branch: `feature/v2.2.1-whitelist-refactor`
- [ ] Verify current config.yaml has whitelist field in S3
- [ ] Review all files using `ROSTER_FILE` env var
- [ ] Document current behavior for rollback

### Prerequisites

- v2.2.0 complete (roster.py exists and works)
- S3 access configured and working
- Whitelist file exists in S3
- Admin credentials available for testing

## Phase 2: Backend Implementation - S3Client Renaming

### Tasks

- [ ] Rename `put_roster()` to `put_whitelist()` in S3Client class
- [ ] Update method docstring
- [ ] Update log message in method
- [ ] Leave `get_roster()` standalone function unchanged (backward compatibility)

### Files to Modify

- `/workspaces/ist256-chatapp/app/dal/s3.py`
  - **Changes**: Rename `put_roster()` method to `put_whitelist()` (lines 96-113)
  - **Lines**: 96-113 (method signature, docstring, log message)
  - **Reason**: Consistent terminology throughout codebase

### Implementation Detail

```python
# Line 96: Change method name
def put_whitelist(self, bucket_name: str, object_key: str, emails: List[str]) -> None:
    """
    Upload whitelist file (comma-separated emails) to S3.  # Line 98: Update docstring

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (whitelist file name)  # Line 102: Update comment
        emails: List of email addresses

    Returns:
        None
    """
    # Join emails with commas (matching format of get_roster)
    content = ",".join(emails)

    # Use existing put_text_file method
    self.put_text_file(bucket_name, object_key, content)
    logger.info(f"Uploaded whitelist to s3://{bucket_name}/{object_key}, email_count={len(emails)}")  # Line 113: Update log
```

## Phase 3: Rename roster.py to whitelist.py

### Tasks

- [ ] Create new whitelist.py file with updated content
- [ ] Rename function: `show_roster()` → `show_whitelist()`
- [ ] Update page title: "Roster Management" → "Whitelist Management"
- [ ] Add info banner showing `config.whitelist` filename
- [ ] Replace `os.environ["ROSTER_FILE"]` with `st.session_state.config.whitelist`
- [ ] Update S3Client method call: `put_roster()` → `put_whitelist()`
- [ ] Update all variable names: roster → whitelist (where makes sense)
- [ ] Update all log messages and UI text
- [ ] Delete old roster.py file (after testing)

### Files to Create

- `/workspaces/ist256-chatapp/app/chat/whitelist.py`
  - **Purpose**: Admin page for whitelist management (renamed from roster.py)
  - **Key changes**:
    - Function name changed
    - Uses `st.session_state.config.whitelist` for filename
    - Displays config filename in info banner
    - All "roster" → "whitelist" in UI and logs

### Files to Delete

- `/workspaces/ist256-chatapp/app/chat/roster.py`
  - **Reason**: Replaced by whitelist.py

### Implementation Structure

```python
import os
import streamlit as st
from loguru import logger

from dal.s3 import S3Client


def show_whitelist():  # Renamed from show_roster
    """Render the Whitelist management page in Streamlit."""
    s3client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )

    st.title("Whitelist Management")  # Changed title
    st.markdown("Manage the whitelist of authorized users.")

    # NEW: Display whitelist filename from config
    whitelist_file = st.session_state.config.whitelist
    st.info(f"📄 Current whitelist file: `{whitelist_file}`")

    # Load current whitelist from S3 (using config)
    try:
        current_whitelist_text = s3client.get_text_file(
            os.environ["S3_BUCKET"],
            whitelist_file  # Changed from os.environ["ROSTER_FILE"]
        )
        emails = [email.strip() for email in current_whitelist_text.split(",") if email.strip()]
        logger.info(f"Loaded whitelist from S3: {len(emails)} emails, file={whitelist_file}")  # Updated log
    except Exception as e:
        st.error(f"Failed to load whitelist from S3: {e}")  # Changed message
        logger.error(f"Failed to load whitelist: {e}")  # Changed log
        emails = []
        current_whitelist_text = ""

    # Display stats
    st.metric("Total Emails in Whitelist", len(emails))  # Changed label

    # Editable text area
    st.header("Edit Whitelist")  # Changed header
    st.markdown("""
    **Instructions:**
    - Enter one email per line or comma-separated
    - Emails will be normalized (trimmed, lowercased) on save
    - Empty lines will be ignored
    """)

    whitelist_input = st.text_area(  # Renamed variable
        "Whitelist Emails",  # Changed label
        value="\n".join(emails),
        height=300,
        help="List of authorized email addresses, one per line"
    )

    # Save button
    col1, col2 = st.columns([1, 3])
    with col1:
        save_button = st.button("💾 Save Whitelist", type="primary")  # Changed label
    with col2:
        if st.button("🔄 Reset to Current"):
            st.rerun()

    if save_button:
        try:
            # Parse input (handle both newline and comma separated)
            input_text = whitelist_input.replace("\n", ",")
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

            # Save to S3 (using config filename and renamed method)
            s3client.put_whitelist(  # Changed from put_roster
                os.environ["S3_BUCKET"],
                whitelist_file,  # Changed from os.environ["ROSTER_FILE"]
                unique_emails
            )

            st.success(f"✅ Whitelist saved successfully! Total emails: {len(unique_emails)}")  # Changed message
            logger.info(f"Admin {st.session_state.auth_model.email} saved whitelist to {whitelist_file} with {len(unique_emails)} emails")  # Updated log

            # Show diff if changed
            if len(unique_emails) != len(emails):
                st.info(f"Email count changed: {len(emails)} → {len(unique_emails)}")

        except Exception as e:
            st.error(f"Failed to save whitelist: {e}")  # Changed message
            logger.error(f"Failed to save whitelist: {e}", exc_info=True)  # Changed log
```

## Phase 4: Update app.py - Authorization and Navigation

### Tasks

- [ ] Update authorization to use `config.whitelist` instead of `ROSTER_FILE`
- [ ] Update admin menu: "Roster" → "Whitelist"
- [ ] Update page routing: import whitelist, call show_whitelist()
- [ ] Update log messages and error messages

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/app.py`
  - **Changes**:
    - Line 133: Change authorization to use `st.session_state.config.whitelist`
    - Line 162: Update admin menu option
    - Lines 324-331: Update page routing
  - **Reason**: Support config-based whitelist and consistent terminology

### Implementation Details

#### Authorization Update (around line 133)

```python
# Before (v2.2.0):
roster_emails = [email.lower().strip() for email in get_roster(
    os.environ["S3_HOST"],
    os.environ["S3_ACCESS_KEY"],
    os.environ["S3_SECRET_KEY"],
    os.environ["S3_BUCKET"],
    os.environ["ROSTER_FILE"]
)]

# After (v2.2.1):
whitelist_file = st.session_state.config.whitelist
whitelist_emails = [email.lower().strip() for email in get_roster(
    os.environ["S3_HOST"],
    os.environ["S3_ACCESS_KEY"],
    os.environ["S3_SECRET_KEY"],
    os.environ["S3_BUCKET"],
    whitelist_file
)]
```

#### Admin Menu Update (line 162)

```python
# Before:
options=["Chat", "Settings", "Export", "Roster", "Session"]

# After:
options=["Chat", "Settings", "Export", "Whitelist", "Session"]
```

#### Page Routing Update (lines 324-331)

```python
# Before:
elif current_page == "Roster":
    try:
        import roster
        roster.show_roster()
        logger.info(f"Admin user {st.session_state.auth_model.email} navigated to Roster")
    except Exception as e:
        st.error("Unable to load Roster page. Try refreshing your browser. If the problem persists, contact mafudge@syr.edu.")
        logger.error(f"Failed to load Roster page: user={st.session_state.auth_model.email}, error={e}", exc_info=True)

# After:
elif current_page == "Whitelist":
    try:
        import whitelist
        whitelist.show_whitelist()
        logger.info(f"Admin user {st.session_state.auth_model.email} navigated to Whitelist")
    except Exception as e:
        st.error("Unable to load Whitelist page. Try refreshing your browser. If the problem persists, contact mafudge@syr.edu.")
        logger.error(f"Failed to load Whitelist page: user={st.session_state.auth_model.email}, error={e}", exc_info=True)
```

## Phase 5: Update session.py - Whitelist Display

### Tasks

- [ ] Update section header: "Roster Users" → "Whitelist Users"
- [ ] Update to use `config.whitelist` with fallback to env var
- [ ] Update source line to show config-based filename
- [ ] Update variable names where appropriate
- [ ] Update log messages and error messages

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/session.py`
  - **Changes**:
    - Lines 17-24: Update whitelist loading logic
    - Lines 57-70: Update expander section
  - **Reason**: Consistent terminology and config-based filename

### Implementation

```python
# Lines 17-27: Update whitelist loading
try:
    # Use config.whitelist if available, fallback to env var for backward compatibility
    whitelist_file = st.session_state.config.whitelist if 'config' in st.session_state else os.environ.get("ROSTER_FILE", "roster.txt")

    whitelist_users = [user.lower().strip() for user in get_roster(  # Renamed variable
        os.environ["S3_HOST"],
        os.environ["S3_ACCESS_KEY"],
        os.environ["S3_SECRET_KEY"],
        os.environ["S3_BUCKET"],
        whitelist_file  # Use config or env var
    ) if user.strip()]
except Exception as e:
    st.error(f"Failed to load whitelist: {e}")  # Changed message
    whitelist_users = []

# Lines 57-70: Update expander section
with st.expander(f"📋 Whitelist Users ({len(whitelist_users)})", expanded=False):  # Changed header
    st.markdown(f"**Source:** `{whitelist_file}` in MinIO S3")  # Use actual filename
    st.markdown("**Access:** Standard chat access (no admin pages)")
    if whitelist_users:
        # Show first 50, with option to see all
        display_count = 50
        for email in whitelist_users[:display_count]:
            st.text(f"• {email}")
        if len(whitelist_users) > display_count:
            if st.button(f"Show all {len(whitelist_users)} emails"):
                for email in whitelist_users[display_count:]:
                    st.text(f"• {email}")
    else:
        st.info("No whitelist users found (empty whitelist)")  # Changed message
```

## Phase 6: Update Documentation and Constants

### Tasks

- [ ] Update VERSION to "2.2.1" in constants.py
- [ ] Update CLAUDE.md to remove ROSTER_FILE env var
- [ ] Add config.whitelist documentation to CLAUDE.md
- [ ] Update utils.py example code (if exists)
- [ ] Audit codebase for remaining "roster" terminology

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/constants.py`
  - **Changes**: Line 1: Update VERSION
  - **Before**: `VERSION="2.2.0"`
  - **After**: `VERSION="2.2.1"`

- `/workspaces/ist256-chatapp/CLAUDE.md`
  - **Changes**:
    - Remove `ROSTER_FILE` from Critical Environment Variables section
    - Add `config.whitelist` to Configuration Files section
    - Update Admin Features section to mention Whitelist (not Roster)
  - **Sections**: Lines ~250 (env vars), ~260 (admin features), ~280 (config)

- `/workspaces/ist256-chatapp/app/utils.py`
  - **Changes**: Line 199: Update example code if it uses `ROSTER_FILE`
  - **Reason**: Keep examples current

### CLAUDE.md Updates

#### Environment Variables Section
```markdown
# Remove this line:
ROSTER_FILE=ist256-fall2025-roster.txt

# No replacement needed - now comes from config
```

#### Configuration Files Section
```markdown
**app/data/config.yaml** (template, actual stored in MinIO S3):
```yaml
configuration:
  ai_model: gpt-4o-mini
  temperature: 0.0
  answer_prompt: "Direct answer mode..."
  tutor_prompt: "Socratic teaching mode..."
  whitelist: "ist256-fall2025-roster.txt"  # Whitelist filename in S3
```
```

#### Admin Features Section
```markdown
# Before:
- **Roster** - edit whitelist/roster directly in app

# After:
- **Whitelist** - edit user whitelist directly in app
```

## Phase 7: Testing

### Manual Testing Checklist

#### S3Client Testing
- [ ] Test `put_whitelist()` method with sample emails
- [ ] Verify saved whitelist can be retrieved with `get_roster()`
- [ ] Confirm method renamed correctly (no `put_roster()` references)

#### Whitelist Page Testing
- [ ] **Access Control**
  - [ ] Admin user can access Whitelist page
  - [ ] Non-admin user cannot access Whitelist page
  - [ ] Menu shows "Whitelist" not "Roster"

- [ ] **Config Integration**
  - [ ] Info banner shows filename from `config.whitelist`
  - [ ] Whitelist loads from config-specified file
  - [ ] Whitelist saves to config-specified file
  - [ ] Error if config.whitelist is empty/missing

- [ ] **Terminology**
  - [ ] Page title says "Whitelist Management"
  - [ ] Buttons say "Save Whitelist"
  - [ ] Metrics say "Emails in Whitelist"
  - [ ] Success messages say "whitelist"
  - [ ] Error messages say "whitelist"
  - [ ] Log messages say "whitelist"

- [ ] **Functionality**
  - [ ] Can add new emails
  - [ ] Can remove emails
  - [ ] Can edit existing emails
  - [ ] Save button works
  - [ ] Reset button works
  - [ ] Saved whitelist persists in S3
  - [ ] Email normalization works
  - [ ] Duplicate removal works
  - [ ] Invalid email warning appears

#### Session Page Testing
- [ ] Section header says "Whitelist Users"
- [ ] Source line shows config-based filename
- [ ] Whitelist users load and display correctly
- [ ] Admin Users section still works
- [ ] Exception Users section still works
- [ ] Fallback to env var if config not loaded

#### Authorization Testing
- [ ] Authorization check uses config.whitelist
- [ ] Users on whitelist can login
- [ ] Users not on whitelist are denied
- [ ] Admin users bypass whitelist check
- [ ] Exception users bypass whitelist check
- [ ] Error message accurate if denied

#### Configuration Testing
- [ ] Config with whitelist field loads correctly
- [ ] Config without whitelist field uses empty string default
- [ ] Can update whitelist filename via Settings page
- [ ] Updated filename used immediately in Whitelist page
- [ ] Settings page displays whitelist field

#### Backward Compatibility Testing
- [ ] `ROSTER_FILE` env var still works as fallback (if config missing)
- [ ] Legacy `get_roster()` function still works
- [ ] Old config.yaml without whitelist field loads gracefully

#### Edge Cases
- [ ] Empty whitelist filename in config (handle gracefully)
- [ ] Whitelist file missing from S3 (error handling)
- [ ] Config not loaded in session (fallback behavior)
- [ ] Very long whitelist filename (UI displays correctly)
- [ ] Special characters in filename (handled correctly)
- [ ] Whitelist field missing from config (uses default)

#### Terminology Audit
- [ ] Search codebase for "roster" (except get_roster function)
- [ ] Verify no UI text says "roster"
- [ ] Verify no log messages say "roster"
- [ ] Verify variable names use "whitelist"
- [ ] Verify function names use "whitelist"

## Phase 8: Documentation

### Tasks

- [ ] Update docs/versions/README.md with v2.2.1 entry
- [ ] Update project_requirements.md (after release)
- [ ] CLAUDE.md updates (see Phase 6)
- [ ] Verify all inline comments updated

### Files to Update

- `/workspaces/ist256-chatapp/docs/versions/README.md`
  - **Changes**: Add v2.2.1 row to version table
  - **Status**: In Development → Released (after deployment)

- `/workspaces/ist256-chatapp/docs/project_requirements.md`
  - **Changes**: Update v2.2.1 status to Released
  - **Release Date**: TBD → actual date (after deployment)

## Phase 9: Cleanup and Final Checks

### Tasks

- [ ] Delete roster.py file (after confirming whitelist.py works)
- [ ] Remove any __pycache__ files for roster.py
- [ ] Search codebase for `ROSTER_FILE` references (document any remaining)
- [ ] Search codebase for "roster" string (ensure only legacy function)
- [ ] Verify no broken imports
- [ ] Run app locally and test all admin pages
- [ ] Check logs for any "roster" references

### Cleanup Commands

```bash
# Remove old roster files
rm /workspaces/ist256-chatapp/app/chat/roster.py
rm -rf /workspaces/ist256-chatapp/app/chat/__pycache__/roster*

# Search for remaining references
grep -r "ROSTER_FILE" /workspaces/ist256-chatapp/app/
grep -r "roster" /workspaces/ist256-chatapp/app/ | grep -v "get_roster"
```

## Phase 10: Deployment

### Tasks

- [ ] Commit changes: "Implement v2.2.1: Whitelist refactoring and bug fixes"
- [ ] Push feature branch to remote
- [ ] Create PR to main branch
- [ ] Code review
- [ ] Address review feedback
- [ ] Merge to main
- [ ] Verify CI/CD pipeline passes
- [ ] Monitor deployment logs
- [ ] Verify whitelist page works in production

### Deployment Checklist

- [ ] All manual tests passing locally
- [ ] No merge conflicts with main
- [ ] VERSION constant updated to "2.2.1"
- [ ] roster.py deleted, whitelist.py created
- [ ] All "Roster" → "Whitelist" in UI
- [ ] `put_roster()` → `put_whitelist()` renamed
- [ ] Authorization uses config.whitelist
- [ ] CLAUDE.md updated
- [ ] No errors in local testing

### Post-Deployment

- [ ] Verify admin can access Whitelist page in production
- [ ] Test saving whitelist in production
- [ ] Verify Session page shows whitelist correctly
- [ ] Monitor logs for "whitelist" (not "roster") terminology
- [ ] Check error logs for issues
- [ ] Notify admins of terminology change

## Dependencies

### Internal Dependencies

- **v2.2.0** (Roster management) must be complete
- **v2.1.0** (AppSettingsModel with whitelist field) must be complete
- Config must exist in S3 with whitelist field
- Admin authentication system must be functional

### External Dependencies

None - uses existing libraries (streamlit, minio, loguru, pydantic)

### Blocked By

None - all prerequisites available

## Risks & Mitigation

### Risk 1: Config missing whitelist field breaks authorization

- **Impact**: High (users cannot login)
- **Probability**: Low (v2.1.0 already handles missing fields)
- **Mitigation**:
  - `AppSettingsModel.from_yaml_string()` uses defaults for missing fields
  - Fallback to env var `ROSTER_FILE` if config not loaded
  - Empty string default for whitelist field
  - Comprehensive error handling and logging

### Risk 2: Admins confused by "Whitelist" vs "Roster" terminology

- **Impact**: Low (minor confusion)
- **Probability**: Medium (term change may be noticed)
- **Mitigation**:
  - Clear documentation in CLAUDE.md
  - Consistent terminology throughout UI
  - Info banner shows filename clearly
  - Error messages are descriptive

### Risk 3: Breaking change if ROSTER_FILE env var removed completely

- **Impact**: Medium (older deployments might break)
- **Probability**: Low (we keep backward compatibility)
- **Mitigation**:
  - Keep `ROSTER_FILE` as fallback option
  - Legacy `get_roster()` function unchanged
  - Session page has fallback logic
  - Document migration path in CLAUDE.md

### Risk 4: Missed "roster" references in codebase

- **Impact**: Low (inconsistent terminology)
- **Probability**: Medium (large codebase)
- **Mitigation**:
  - Comprehensive grep search in Phase 9
  - Manual testing checklist includes terminology audit
  - Code review catches remaining references
  - Phase 9 cleanup ensures completeness

## Success Criteria

- [ ] Whitelist page accessible from admin menu (not "Roster")
- [ ] Whitelist page displays config.whitelist filename
- [ ] Admin can load and save whitelist using config filename
- [ ] Session page shows "Whitelist Users" with config-based filename
- [ ] Authorization uses config.whitelist correctly
- [ ] `put_whitelist()` method works correctly
- [ ] roster.py deleted, whitelist.py created
- [ ] All UI text says "whitelist" (not "roster")
- [ ] All log messages say "whitelist" (not "roster")
- [ ] `ROSTER_FILE` env var removed from documentation
- [ ] VERSION displays "2.2.1" in UI
- [ ] No errors in production logs
- [ ] Whitelist changes persist across sessions
- [ ] All manual tests pass
- [ ] Backward compatibility maintained (fallback works)

## Rollback Procedure

1. **Identify issue**
   - Check logs for exceptions
   - Verify user reports

2. **Rollback code**
   - `git revert <v2.2.1-commit-hash>`
   - Deploy reverted version

3. **Whitelist data**
   - Whitelist file in S3 is unaffected by code rollback
   - Config.yaml in S3 unchanged (whitelist field optional)
   - `ROSTER_FILE` env var still works (backward compatible)

4. **Verify rollback**
   - Admin menu shows "Roster" option (not "Whitelist")
   - roster.py file exists (whitelist.py removed)
   - Authorization still works
   - Session page shows roster users

5. **Communication**
   - Notify admins of rollback
   - Document issue for future fix

## Post-Deployment

### Monitoring

Monitor for first 24-48 hours:
- Application error logs (loguru output)
- Authorization errors (whitelist-related)
- Admin usage of Whitelist page
- User login issues

### Key Metrics

- No increase in error rate
- Whitelist page load time (<2 seconds)
- Save operations successful (100%)
- No authorization failures due to config issues

### Follow-up Tasks

- [ ] Gather admin feedback on terminology change
- [ ] Consider removing `ROSTER_FILE` fallback in future version
- [ ] Document migration guide for other deployments
- [ ] Update training documentation for admins

---

**Generated**: 2026-01-13
**Author**: AI-assisted planning via /design command
**Version**: 2.2.1
