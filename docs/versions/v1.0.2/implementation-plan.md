# Implementation Plan: Authentication & Authorization Foundation - v1.0.2

## Timeline

- Estimated effort: 4-6 hours
- Complexity: Medium
- Suggested sprint: 1 day

## Phase 1: Preparation

### Tasks

- [ ] Review technical specification for v1.0.2
- [ ] Set up development branch: `feature/v1.0.2-authentication`
- [ ] Review existing authentication code in app.py (lines 50-102)
- [ ] Verify all environment variables are set in .env file
- [ ] Test current appnew.py to understand baseline functionality

### Prerequisites

- Azure AD application configured (MSAL_CLIENT_ID, MSAL_AUTHORITY)
- MinIO S3 accessible with roster file uploaded
- All required environment variables in .env file
- streamlit_msal library installed (already in requirements.txt)

## Phase 2: Backend Implementation

### Tasks

- [ ] Import required modules at top of appnew.py
- [ ] Add MSAL authentication initialization
- [ ] Add AuthModel creation from auth_data
- [ ] Implement roster loading from S3
- [ ] Implement user type validation hierarchy
- [ ] Add session state storage for auth data

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/appnew.py`
  - **Changes**: Add authentication system after page config (after line 60)
  - **Lines**: Insert ~40-50 lines of auth code
  - **Reason**: Establish user identity and access control before chat interface

**Specific Implementation Steps**:

1. **Add imports** (after line 12):
```python
from streamlit_msal import Msal
from dal.models import AuthModel
from utils import get_roster
```

2. **Add MSAL initialization** (after line 66, before existing sidebar content):
```python
# ----------------- Authentication -----------------
if 'auth_data' not in st.session_state:
    with st.sidebar:
        auth_data = Msal.initialize_ui(
            client_id=os.environ["MSAL_CLIENT_ID"],
            authority=os.environ["MSAL_AUTHORITY"]
        )

        if auth_data is None:
            st.warning("Please sign in with your Syracuse University account to continue.")
            st.stop()

        st.session_state.auth_data = auth_data
        st.session_state.auth_model = AuthModel.from_auth_data(auth_data)
```

3. **Add roster validation** (after auth_data initialization):
```python
# ----------------- Authorization -----------------
if 'validated' not in st.session_state:
    email = st.session_state.auth_model.email

    # Load lists
    admin_users = os.environ["ADMIN_USERS"].split(",")
    exception_users = os.environ["ROSTER_EXCEPTION_USERS"].split(",")
    valid_users = get_roster(
        os.environ["S3_HOST"],
        os.environ["S3_ACCESS_KEY"],
        os.environ["S3_SECRET_KEY"],
        os.environ["S3_BUCKET"],
        os.environ["ROSTER_FILE"]
    )

    # Validate user type
    if email in admin_users:
        st.session_state.validated = "admin"
    elif email in exception_users:
        st.session_state.validated = "exception"
    elif email in valid_users:
        st.session_state.validated = "roster"
    else:
        with st.sidebar:
            st.error(f"Access denied. Email {email} not found in roster: {os.environ['ROSTER_FILE']}")
            st.info("Please contact your instructor if you believe this is an error.")
        st.session_state.clear()
        st.stop()
```

### Files to Create

None - all code integrated into existing appnew.py.

## Phase 3: Frontend Implementation

### Tasks

- [ ] Ensure sign-in UI appears in sidebar
- [ ] Test sign-in button functionality
- [ ] Verify error messages display correctly
- [ ] Ensure chat interface only loads after authentication

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/appnew.py`
  - **Changes**: Authentication UI in sidebar (already handled by Msal.initialize_ui)
  - **Streamlit components**: st.warning(), st.error(), st.info(), st.stop()

**No new Streamlit components needed** - Msal.initialize_ui() provides the sign-in button automatically.

### Files to Create

None.

## Phase 4: Configuration & Constants

### Tasks

- [ ] Update `app/chat/constants.py` with VERSION = "1.0.2"
- [ ] Verify all environment variables documented
- [ ] No config.yaml changes needed (loaded in v1.0.4)

### Configuration Changes

**constants.py**:
```python
VERSION="1.0.2"  # Update from "1.0.1"
```

**No other configuration changes** needed for this version.

## Phase 5: Testing

### Tasks

- [ ] Manual testing checklist
  - [ ] Test admin user login (email in ADMIN_USERS)
  - [ ] Test exception user login (email in ROSTER_EXCEPTION_USERS)
  - [ ] Test roster user login (email in roster file)
  - [ ] Test unauthorized user (email not in any list)
  - [ ] Test session persistence (refresh page after login)
  - [ ] Test logout (clear session state)
  - [ ] Test with missing MSAL environment variables
  - [ ] Test with missing roster file in S3
- [ ] Integration testing
  - [ ] Azure AD OAuth2 flow completes successfully
  - [ ] MinIO S3 roster loading works
  - [ ] Session state persists across interactions
- [ ] Performance testing
  - [ ] Login time < 3 seconds
  - [ ] Roster loading < 1 second
  - [ ] No lag after authentication

### Test Data

**Test Accounts**:
- Admin user: mafudge@syr.edu (in ADMIN_USERS)
- Exception user: ndlyga@syr.edu (in ROSTER_EXCEPTION_USERS)
- Roster user: student@syr.edu (in roster file)
- Unauthorized user: unauthorized@syr.edu (not in any list)

**Roster File**:
- Create test roster file with 5-10 email addresses
- Upload to MinIO S3 in ist256chatapp bucket
- Filename: `ist256-test-roster.txt`

## Phase 6: Documentation

### Tasks

- [ ] Update CLAUDE.md with authentication section (optional for v1.0.2)
- [ ] Add inline code comments for authentication logic
- [ ] Document environment variables in .env.example (if exists)
- [ ] Update docs/versions/README.md with v1.0.2 entry

### Documentation Files

- `CLAUDE.md` - Optional update to mention authentication in appnew.py
- `docs/versions/README.md` - Add v1.0.2 row to version table
- Inline comments in appnew.py for clarity

## Phase 7: Deployment

### Tasks

- [ ] Commit changes with message: "Implement v1.0.2: Authentication & Authorization Foundation"
- [ ] Push feature branch to remote
- [ ] Test in development environment
- [ ] Create PR to ui-upgrade branch (or main)
- [ ] Code review
- [ ] Address review feedback
- [ ] Merge to ui-upgrade branch
- [ ] Monitor for authentication issues

### Deployment Checklist

- [ ] All manual tests passing
- [ ] No merge conflicts with ui-upgrade branch
- [ ] VERSION constant updated to "1.0.2"
- [ ] Environment variables documented
- [ ] No breaking changes to existing app.py

### Deployment Command

```bash
# From feature branch
git add app/chat/appnew.py app/chat/constants.py docs/versions/
git commit -m "Implement v1.0.2: Authentication & Authorization Foundation

- Add MSAL authentication to appnew.py
- Implement roster/whitelist validation
- Support admin, exception, and roster user types
- Session-based authorization
- Error handling for unauthorized users

🤖 Generated with Claude Code (https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push origin feature/v1.0.2-authentication
```

## Dependencies

### Internal Dependencies

- None (first step in v2.0 migration)

### External Dependencies

- Azure AD application configured and accessible
- MinIO S3 server running with roster file uploaded
- Environment variables configured in .env

### Team Dependencies

- Admin to provide MSAL_CLIENT_ID and MSAL_AUTHORITY
- Admin to upload roster file to S3
- Testing coordination for different user types

## Risks & Mitigation

### Risk 1: OAuth2 redirect breaks in production

- **Impact**: High - users cannot log in
- **Probability**: Medium
- **Mitigation**:
  - Test OAuth2 flow in dev environment first
  - Ensure redirect URIs configured in Azure AD
  - Keep app.py functional as fallback

### Risk 2: Roster file not accessible from S3

- **Impact**: Medium - all users denied access
- **Probability**: Low
- **Mitigation**:
  - Test S3 connectivity before deployment
  - Add error handling to allow access if roster file missing
  - Log warnings when roster cannot be loaded

### Risk 3: Session state cleared unexpectedly

- **Impact**: Medium - users logged out randomly
- **Probability**: Low
- **Mitigation**:
  - Test session persistence thoroughly
  - Understand Streamlit session lifecycle
  - Document known limitations

### Risk 4: MSAL library conflicts with new UI

- **Impact**: Medium - UI breaks or auth fails
- **Probability**: Low
- **Mitigation**:
  - Test MSAL with streamlit-extras.bottom_container
  - Verify sidebar rendering with MSAL button
  - Isolate auth code from chat UI

## Success Criteria

- [ ] Admin users can log in and see validated="admin"
- [ ] Exception users can log in and see validated="exception"
- [ ] Roster users can log in and see validated="roster"
- [ ] Unauthorized users see error and cannot access chat
- [ ] Session persists across page refreshes
- [ ] Sign-in button appears correctly in sidebar
- [ ] Error messages are clear and helpful
- [ ] VERSION constant updated to "1.0.2"
- [ ] No regressions in existing appnew.py functionality (mode/context selection)
- [ ] Authentication completes in < 3 seconds

## Rollback Procedure

1. **Identify the issue**:
   - Authentication not working?
   - Users denied incorrectly?
   - App crashes on auth?

2. **Immediate rollback**:
   ```bash
   git revert <commit-hash>
   git push origin ui-upgrade --force
   ```

3. **Verify app.py still works**:
   - Old interface should remain functional
   - Users can continue using app.py

4. **Investigate and fix**:
   - Check environment variables
   - Verify Azure AD configuration
   - Test MinIO S3 connectivity
   - Review error logs

5. **Redeploy when fixed**:
   - Create new branch
   - Fix identified issues
   - Retest thoroughly
   - Deploy again

## Post-Deployment

### Monitoring

- **Watch for authentication errors**:
  - Users unable to log in
  - OAuth2 redirects failing
  - Session state issues

- **Monitor S3 connectivity**:
  - Roster loading failures
  - Timeout errors

- **Track user types**:
  - How many admin vs roster users?
  - Any unauthorized access attempts?

### Follow-up Tasks

- [ ] Gather user feedback on login experience
- [ ] Optimize roster loading (cache at server level if needed)
- [ ] Consider adding "Sign Out" button to sidebar
- [ ] Prepare for v1.0.3 (database & logging integration)

---

**Generated**: 2025-12-27
**Author**: AI-assisted planning via /design command
**Version**: 1.0.2
