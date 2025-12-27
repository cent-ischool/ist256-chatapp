# Technical Specification: Authentication & Authorization Foundation - v1.0.2

## Overview

Version 1.0.2 establishes the authentication and authorization foundation for the new chat interface (appnew.py). This version ports the complete MSAL authentication system from app.py, including roster/whitelist validation and user type detection. This is the critical first step in migrating to the v2.0 architecture, enabling secure user access while maintaining the new UI/UX paradigm with mode selection and always-on context injection.

## Architecture Changes

### Components Affected

- `/workspaces/ist256-chatapp/app/chat/appnew.py` - Add complete authentication system (lines 50-102 from app.py)
- `/workspaces/ist256-chatapp/app/chat/constants.py` - Update VERSION to "1.0.2"

### New Components

No new files created. All authentication logic integrated into existing appnew.py.

### Dependencies

**External Libraries** (already in requirements.txt):
- `streamlit_msal` - Microsoft authentication for Streamlit
- `pydantic` - Data validation for AuthModel

**Internal Modules**:
- `/workspaces/ist256-chatapp/app/dal/models.py` - AuthModel class
- `/workspaces/ist256-chatapp/app/utils.py` - get_roster() helper function

## Data Models

### Database Changes

No database changes required. Authentication is session-based.

### API Changes

No API changes. Uses Microsoft Azure AD OAuth2 flow via streamlit_msal.

## Technical Design

### Backend Implementation

**Authentication Flow** (from app.py lines 50-82):

```python
1. MSAL Initialization:
   - Load MSAL_CLIENT_ID and MSAL_AUTHORITY from environment
   - Initialize streamlit_msal.Msal object
   - Render sign-in button in sidebar

2. OAuth2 Flow:
   - User clicks "Sign In" button
   - Redirects to Microsoft login page
   - Returns auth_data dict on successful authentication

3. AuthModel Creation:
   - Extract session_id from localAccountId
   - Extract email from idTokenClaims.preferred_username
   - Extract name from idTokenClaims.name
   - Parse firstname as first word of name
   - Store in st.session_state.auth_model

4. Roster Validation Hierarchy:
   a. Load roster from MinIO S3 (get_roster function)
   b. Check if user in ADMIN_USERS → set validated="admin"
   c. Check if user in ROSTER_EXCEPTION_USERS → set validated="exception"
   d. Check if user in roster file → set validated="roster"
   e. If none match → show error and st.stop()

5. Session State Storage:
   - st.session_state.auth_data (MSAL response)
   - st.session_state.auth_model (AuthModel instance)
   - st.session_state.validated (user type: admin/exception/roster)
```

**Roster Loading** (from utils.py):

```python
def get_roster(host_port, access_key, secret_key, bucket, object_key):
    # Creates temporary MinIO client
    # Downloads roster file from S3
    # Parses CSV of email addresses
    # Returns list of valid_users
```

### Frontend Implementation

**Sidebar Changes** (in appnew.py after line 67):

```python
# Add before existing sidebar content
if 'auth_data' not in st.session_state:
    with st.sidebar:
        auth_data = Msal.initialize_ui(
            client_id=os.environ["MSAL_CLIENT_ID"],
            authority=os.environ["MSAL_AUTHORITY"]
        )

        if auth_data is None:
            st.warning("Please sign in to continue")
            st.stop()

        st.session_state.auth_data = auth_data
        st.session_state.auth_model = AuthModel.from_auth_data(auth_data)

# Roster validation (after authentication)
if 'validated' not in st.session_state:
    email = st.session_state.auth_model.email

    # Load roster from S3
    valid_users = get_roster(...)

    # Check user type
    if email in admin_users:
        st.session_state.validated = "admin"
    elif email in exception_users:
        st.session_state.validated = "exception"
    elif email in valid_users:
        st.session_state.validated = "roster"
    else:
        st.error(f"Access denied. Email {email} not in roster.")
        st.session_state.clear()
        st.stop()
```

**No UI Changes** to existing chat interface. Authentication happens before chat loads.

### Integration Points

**MinIO S3 Integration**:
- Roster file stored in S3 bucket (e.g., `ist256-fall2025-roster.txt`)
- Loaded at authentication time via get_roster()
- Requires S3_HOST, S3_ACCESS_KEY, S3_SECRET_KEY, S3_BUCKET, ROSTER_FILE env vars

**Session State Integration**:
- auth_data and auth_model available throughout appnew.py
- validated user type used for future admin features (v1.0.7)
- Persists across page refreshes via Streamlit session

**No Database Integration** yet (comes in v1.0.3)

**No LLM Integration** yet (comes in v1.0.4)

## Configuration

### Environment Variables

**Required (must be set):**

- `MSAL_CLIENT_ID` - Azure AD application client ID
  - Example: `f6958edd-646f-4e84-895a-ede5aa18036e`

- `MSAL_AUTHORITY` - Azure AD authority URL
  - Example: `https://login.microsoftonline.com/4278a402-1a9e-4eb9-8414-ffb55a5fcf1e`

- `ADMIN_USERS` - Comma-separated list of admin emails
  - Example: `mafudge@syr.edu,admin@example.com`

- `ROSTER_EXCEPTION_USERS` - Comma-separated list of exception emails
  - Example: `ndlyga@syr.edu,jmstanto@syr.edu`

- `S3_HOST` - MinIO S3 host and port
  - Example: `nas.home.michaelfudge.com:9000`

- `S3_BUCKET` - S3 bucket name
  - Example: `ist256chatapp`

- `S3_ACCESS_KEY` - S3 access key
  - Example: `minioadmin`

- `S3_SECRET_KEY` - S3 secret key
  - Example: `<secret>`

- `ROSTER_FILE` - Roster filename in S3
  - Example: `ist256-fall2025-roster.txt`

### Config Files

No changes to config.yaml or prompts.yaml. Those are loaded in later versions (v1.0.4).

## Security Considerations

**Authentication**:
- Uses Microsoft Azure AD OAuth2 (industry standard)
- Tokens managed by streamlit_msal library
- No passwords stored locally

**Authorization**:
- Three-tier access control: admin, exception, roster
- Roster stored securely in S3 (not in code)
- Email-based validation (no PII beyond email)

**Data Privacy**:
- Email, name, firstname stored in session state (temporary)
- Session clears on logout
- No persistent storage of user credentials

**Input Validation**:
- Email validated by Azure AD
- Roster file parsed as simple text (low injection risk)

**Access Control**:
- Unauthorized users blocked with st.stop()
- Session cleared on access denial
- Error message includes roster filename for transparency

## Performance Considerations

**Authentication Performance**:
- OAuth2 redirect adds ~1-2 seconds to first load
- Subsequent page loads use cached session (no re-auth)

**Roster Loading**:
- Roster loaded once per session (cached in session state)
- MinIO S3 call typically <100ms
- Roster file size: ~100 emails = <5KB

**Scalability**:
- Session-based auth scales with Streamlit's session management
- No database queries for authentication
- S3 can handle high concurrent reads

**Memory Usage**:
- AuthModel: ~1KB per user session
- Roster list: ~5KB cached per session
- Minimal memory footprint

## Error Handling

**Expected Errors**:

1. **User not in roster**:
   - Error message: "Access denied. Email [email] not in roster [filename]."
   - Action: Clear session, stop app
   - User sees helpful error with roster filename

2. **MSAL environment variables missing**:
   - Error: KeyError on MSAL_CLIENT_ID or MSAL_AUTHORITY
   - Action: App crashes with clear error
   - Admin must configure environment

3. **S3 roster file not found**:
   - Error: MinIO client exception
   - Action: Allow access (empty roster = allow all)
   - Log warning

4. **OAuth2 flow failure**:
   - Error: auth_data returns None
   - Action: Show "Please sign in" warning, stop app
   - User can retry sign-in

**User-Facing Messages**:
- Simple, clear error messages
- Include actionable information (e.g., roster filename)
- No technical jargon

**Logging**:
- No logging in this version (comes in v1.0.6)
- Errors display in Streamlit UI

## Testing Strategy

### Manual Testing

- [ ] **Admin user login**
  - Sign in with email in ADMIN_USERS
  - Verify validated="admin" in session state
  - Verify app loads successfully

- [ ] **Exception user login**
  - Sign in with email in ROSTER_EXCEPTION_USERS
  - Verify validated="exception"
  - Verify app loads

- [ ] **Roster user login**
  - Sign in with email in roster file
  - Verify validated="roster"
  - Verify app loads

- [ ] **Unauthorized user**
  - Sign in with email NOT in any list
  - Verify error message displays
  - Verify session cleared
  - Verify app stops

- [ ] **Missing MSAL env vars**
  - Remove MSAL_CLIENT_ID temporarily
  - Verify app crashes with clear KeyError
  - Restore environment variable

- [ ] **Session persistence**
  - Log in successfully
  - Refresh page (F5)
  - Verify still authenticated (no re-login)

- [ ] **Logout and re-login**
  - Clear session state
  - Verify prompted to sign in again

### Integration Testing

- [ ] **MinIO S3 integration**
  - Verify roster file loads from S3
  - Test with valid and invalid bucket names
  - Test with missing roster file

- [ ] **Azure AD integration**
  - Test OAuth2 flow with real Azure AD account
  - Verify token refresh if needed
  - Test with different user types

### Edge Cases

- [ ] Empty roster file (allow all or deny all?)
- [ ] Roster file with invalid email formats
- [ ] User in multiple lists (admin + roster)
- [ ] Very long roster file (1000+ emails)
- [ ] Special characters in email addresses

## Rollback Plan

### Rollback Procedure

1. **Revert appnew.py changes**:
   ```bash
   git revert <commit-hash>
   git push origin ui-upgrade
   ```

2. **Verify old app.py still works**:
   - app.py unchanged, should still function
   - Users can continue using old interface

3. **Clear environment variables** (if needed):
   - Remove MSAL_* variables if causing issues
   - Restore from backup .env file

No database rollback needed (no database changes).

## References

- Azure AD MSAL Documentation: https://docs.microsoft.com/en-us/azure/active-directory/develop/msal-overview
- streamlit_msal Library: https://github.com/conradbez/streamlit-msal
- Existing Implementation: `/workspaces/ist256-chatapp/app/chat/app.py` lines 50-102
- Utility Functions: `/workspaces/ist256-chatapp/app/utils.py`

---

**Generated**: 2025-12-27
**Author**: AI-assisted design via /design command
**Version**: 1.0.2
