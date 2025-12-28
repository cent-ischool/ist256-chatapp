# Implementation Plan: S3 Config Fallback Error Handling - v2.0.1

## Timeline

- Estimated effort: 2-3 hours
- Complexity: Low
- Suggested sprint: Single development session

## Phase 1: Preparation

### Tasks

- [x] Review technical specification
- [ ] Set up development branch: `feature/v2.0.1-s3-fallback`
- [ ] Update TODO.txt with version tasks (if applicable)
- [ ] Verify all dependencies are available (loguru, minio)
- [ ] Review existing code patterns in app/dal/s3.py

### Prerequisites

- Python environment with existing dependencies installed
- Access to codebase at `/workspaces/ist256-chatapp/`
- Test environment with S3 access (for testing)

## Phase 2: Backend Implementation

### Tasks

- [ ] Modify `get_text_file()` method in S3Client class
- [ ] Add fallback_file_path parameter with default None
- [ ] Implement try-except block around S3 fetch
- [ ] Add fallback file loading logic
- [ ] Add appropriate logging statements
- [ ] Test method in isolation (manual testing)

### Files to Modify

- `/workspaces/ist256-chatapp/app/dal/s3.py`
  - **Changes**: Update `get_text_file()` method signature and implementation
  - **Lines**: 33-37 (current implementation)
  - **Reason**: Add robust error handling with fallback mechanism
  - **Specific Changes**:
    1. Add `fallback_file_path: str = None` parameter to method signature
    2. Wrap existing logic in try-except block
    3. In except block, check if fallback_file_path is provided
    4. If provided, log error and load from local file
    5. If not provided, re-raise exception
    6. Add logger.error() for S3 failures
    7. Add logger.info() for fallback file usage

### Files to Create

None - this is a modification only.

### Implementation Details

**Before (lines 33-37):**
```python
def get_text_file(self, bucket_name: str, object_key: str) -> str:
    response = self.client.get_object(bucket_name, object_key)
    file_content = response.read().decode('utf-8')
    logger.info(f"Fetched text file s3://{bucket_name}/{object_key}, size={len(file_content)} characters")
    return file_content
```

**After:**
```python
def get_text_file(self, bucket_name: str, object_key: str, fallback_file_path: str = None) -> str:
    try:
        response = self.client.get_object(bucket_name, object_key)
        file_content = response.read().decode('utf-8')
        logger.info(f"Fetched text file s3://{bucket_name}/{object_key}, size={len(file_content)} characters")
        return file_content
    except Exception as e:
        if fallback_file_path:
            logger.error(f"Failed to fetch s3://{bucket_name}/{object_key}: {e}")
            logger.info(f"Using fallback file: {fallback_file_path}")
            with open(fallback_file_path, 'r', encoding='utf-8') as f:
                fallback_content = f.read()
            logger.info(f"Loaded fallback file {fallback_file_path}, size={len(fallback_content)} characters")
            return fallback_content
        else:
            logger.error(f"Failed to fetch s3://{bucket_name}/{object_key} and no fallback provided: {e}")
            raise
```

## Phase 3: Frontend Implementation

### Tasks

- [ ] Update get_text_file() calls in app.py to include fallback paths
- [ ] Update get_text_file() calls in app_v1.py to include fallback paths
- [ ] Update get_text_file() calls in settings.py to include fallback paths
- [ ] Update get_text_file() calls in prompts.py to include fallback path
- [ ] Verify no other call sites exist (grep for get_text_file)

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/app.py`
  - **Changes**: Add fallback file paths to get_text_file() calls
  - **Lines**: 236-237
  - **Before**:
    ```python
    config_yaml = st.session_state.s3_client.get_text_file(os.environ["S3_BUCKET"], os.environ["CONFIG_FILE"])
    prompts_yaml = st.session_state.s3_client.get_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"])
    ```
  - **After**:
    ```python
    config_yaml = st.session_state.s3_client.get_text_file(
        os.environ["S3_BUCKET"],
        os.environ["CONFIG_FILE"],
        fallback_file_path="app/data/config.yaml"
    )
    prompts_yaml = st.session_state.s3_client.get_text_file(
        os.environ["S3_BUCKET"],
        os.environ["PROMPTS_FILE"],
        fallback_file_path="app/data/prompts.yaml"
    )
    ```

- `/workspaces/ist256-chatapp/app/chat/app_v1.py`
  - **Changes**: Add fallback file paths to get_text_file() calls
  - **Lines**: 145-146
  - **Same pattern as app.py above**

- `/workspaces/ist256-chatapp/app/chat/settings.py`
  - **Changes**: Add fallback file paths to get_text_file() calls
  - **Lines**: 16-17
  - **Same pattern as app.py above**

- `/workspaces/ist256-chatapp/app/chat/prompts.py`
  - **Changes**: Add fallback file path to get_text_file() call
  - **Lines**: 17
  - **Before**:
    ```python
    prompts_yaml = s3client.get_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"])
    ```
  - **After**:
    ```python
    prompts_yaml = s3client.get_text_file(
        os.environ["S3_BUCKET"],
        os.environ["PROMPTS_FILE"],
        fallback_file_path="app/data/prompts.yaml"
    )
    ```

### Files to Create

None - no new pages needed.

## Phase 4: Configuration & Constants

### Tasks

- [ ] Update `app/chat/constants.py` with VERSION = "v2.0.1"
- [ ] Verify fallback files exist at expected paths
- [ ] (Optional) Add CONFIG_FILE_FALLBACK and PROMPTS_FILE_FALLBACK env vars to .env.example
- [ ] (Optional) Document new env vars in CLAUDE.md

### Configuration Changes

- **Update VERSION constant:**
  - File: `/workspaces/ist256-chatapp/app/chat/constants.py`
  - Line: 1
  - Change: `VERSION="2.0.0"` → `VERSION="v2.0.1"`

- **Verify fallback files exist:**
  - `/workspaces/ist256-chatapp/app/data/config.yaml` (should exist)
  - `/workspaces/ist256-chatapp/app/data/prompts.yaml` (should exist)

- **Optional environment variables:**
  - Not strictly necessary (hardcoded paths are fine)
  - If desired for flexibility, add to .env.example:
    ```
    CONFIG_FILE_FALLBACK=app/data/config.yaml
    PROMPTS_FILE_FALLBACK=app/data/prompts.yaml
    ```

## Phase 5: Testing

### Tasks

- [ ] Manual testing checklist
  - [ ] Test Case 1: Normal S3 operation (files in S3)
  - [ ] Test Case 2: S3 files missing (fallback triggered)
  - [ ] Test Case 3: S3 service unavailable (fallback triggered)
  - [ ] Test Case 4: Fallback files missing (app should crash gracefully)
  - [ ] Test Case 5: Admin can still modify settings and save to S3
  - [ ] Test Case 6: Non-admin user experience unchanged
- [ ] Integration testing
  - [ ] Database integration (no changes, should work as before)
  - [ ] S3 integration (test both success and failure paths)
  - [ ] LLM API integration (unchanged, should work as before)
- [ ] Error message validation
  - [ ] Check logs for appropriate error messages
  - [ ] Check logs for fallback usage messages

### Test Data

- Test S3 bucket: Use existing development S3 bucket
- Test fallback files: Use existing files in app/data/
- Test scenarios:
  1. Temporarily rename S3 files to simulate missing files
  2. Change S3_HOST env var to invalid host to simulate connection failure
  3. Temporarily rename fallback files to test error handling

### Detailed Test Procedures

**Test Case 1: Normal S3 Operation**
1. Ensure S3 files exist: config.yaml and prompts.yaml in S3 bucket
2. Start application: `streamlit run app/chat/app.py`
3. Observe logs for: "Fetched text file s3://..."
4. Verify app loads successfully
5. Check settings page shows correct config from S3
6. Expected result: No fallback messages in logs

**Test Case 2: S3 Files Missing**
1. Using MinIO console or s3cmd, rename config.yaml to config.yaml.bak in S3
2. Rename prompts.yaml to prompts.yaml.bak in S3
3. Start application: `streamlit run app/chat/app.py`
4. Observe logs for: "Failed to fetch s3://...", "Using fallback file: app/data/..."
5. Verify app loads successfully
6. Test chat functionality
7. Restore S3 files (rename back)
8. Expected result: App works, fallback files used

**Test Case 3: S3 Service Unavailable**
1. Edit .env: Change S3_HOST to invalid value (e.g., "invalid.host.com:9000")
2. Start application: `streamlit run app/chat/app.py`
3. Wait for connection timeout (may take 10-30 seconds)
4. Observe logs for connection error and fallback usage
5. Verify app loads successfully
6. Restore S3_HOST in .env
7. Expected result: App works after timeout, fallback files used

**Test Case 4: Fallback Files Missing**
1. Rename app/data/config.yaml to config.yaml.bak
2. Ensure S3 is unavailable (invalid host) or files missing
3. Start application: `streamlit run app/chat/app.py`
4. Observe traceback with FileNotFoundError
5. App should fail to start
6. Restore app/data/config.yaml
7. Expected result: App crashes with clear error message

**Test Case 5: Admin Settings Page**
1. Ensure S3 is operational with files present
2. Start app and login as admin user
3. Navigate to Settings page via admin menu
4. Modify ai_model or temperature
5. Click "Save Configuration"
6. Restart app
7. Verify modified settings persist (loaded from S3, not fallback)
8. Expected result: S3 files take precedence over fallback

**Test Case 6: Non-Admin User**
1. Start app with either S3 or fallback files
2. Login as non-admin roster user
3. Select mode and context
4. Send chat message
5. Verify response received
6. Expected result: No difference in user experience

## Phase 6: Documentation

### Tasks

- [ ] Update CLAUDE.md with error handling details (optional - minor change)
- [ ] Add inline code comments for fallback logic in s3.py
- [ ] Update version in docs/versions/README.md
- [ ] (Optional) Add troubleshooting section to README.md

### Documentation Files

- `/workspaces/ist256-chatapp/CLAUDE.md`
  - Optional update to "Important Files" section mentioning fallback files
  - Add note in "Configuration Files" section about fallback mechanism

- `/workspaces/ist256-chatapp/app/dal/s3.py`
  - Add docstring to `get_text_file()` method explaining fallback parameter
  - Add inline comment explaining fallback logic

- `/workspaces/ist256-chatapp/docs/versions/README.md`
  - Add entry for v2.0.1 in version history table

### Documentation Example

**Docstring for get_text_file():**
```python
def get_text_file(self, bucket_name: str, object_key: str, fallback_file_path: str = None) -> str:
    """
    Fetch a text file from S3, with optional local fallback.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (file path) in bucket
        fallback_file_path: Optional local file path to use if S3 fetch fails

    Returns:
        File content as UTF-8 string

    Raises:
        Exception: If S3 fetch fails and no fallback provided
        FileNotFoundError: If S3 fetch fails and fallback file doesn't exist

    Note:
        If S3 fetch fails and fallback is provided, errors are logged and
        fallback file is loaded transparently.
    """
```

## Phase 7: Deployment

### Tasks

- [ ] Commit changes with message: "Implement v2.0.1: S3 config fallback error handling"
- [ ] Push feature branch to remote
- [ ] Create PR to main branch
- [ ] Code review
- [ ] Address review feedback
- [ ] Merge to main
- [ ] Verify CI/CD pipeline passes
- [ ] Monitor deployment
- [ ] Verify in production environment

### Deployment Checklist

- [ ] All tests passing (manual tests completed)
- [ ] No merge conflicts with main branch
- [ ] Version number updated in constants.py
- [ ] Documentation complete (technical spec, implementation plan)
- [ ] No breaking changes (backward compatible)
- [ ] Fallback files committed to git in app/data/
- [ ] S3 files uploaded to production bucket (recommended but not required)

### Commit Message Format

```
Implement v2.0.1: S3 config fallback error handling

- Modified S3Client.get_text_file() to accept fallback_file_path parameter
- Added try-except block to handle S3 fetch failures gracefully
- Implemented local file fallback when S3 unavailable
- Updated all call sites in app.py, app_v1.py, settings.py, prompts.py
- Added comprehensive logging for S3 errors and fallback usage
- Updated VERSION to v2.0.1 in constants.py

Fixes crash when S3 config files unavailable. App now starts with
local fallback files when S3 is down or files are missing.
```

## Dependencies

### Internal Dependencies

- Depends on: v2.0.0 (current version)
- Blocks: None (patch version, independent)

### External Dependencies

- Python standard library: `open()` for file I/O
- Existing: `loguru` for logging
- Existing: `minio` for S3 client

### Team Dependencies

- None - single developer can complete

## Risks & Mitigation

### Risk 1: Fallback files out of sync with S3

- **Impact**: Medium
- **Probability**: Low to Medium
- **Mitigation**:
  - Document that fallback files should be kept in sync with S3 defaults
  - Consider adding a comment in fallback files: "# Fallback copy - keep in sync with S3"
  - Admin should update both S3 and git when making config changes

### Risk 2: Silent failures if fallback always used

- **Impact**: Low
- **Probability**: Low
- **Mitigation**:
  - Log S3 errors at ERROR level so admins notice in logs
  - Log fallback usage at INFO level for visibility
  - Admins should monitor logs for "Failed to fetch s3://" messages

### Risk 3: Fallback files deleted from git

- **Impact**: High (app won't start)
- **Probability**: Very Low
- **Mitigation**:
  - Document importance of fallback files in CLAUDE.md
  - Keep fallback files in git with clear purpose
  - CI/CD should fail if fallback files missing (future enhancement)

### Risk 4: Environment-specific paths

- **Impact**: Medium
- **Probability**: Low
- **Mitigation**:
  - Use relative paths ("app/data/config.yaml") that work from project root
  - Document working directory assumptions
  - Consider using absolute paths if issues arise

## Success Criteria

- [x] All tasks completed
- [ ] Version number updated in constants.py to v2.0.1
- [ ] All manual tests passing
- [ ] Documentation updated (technical spec, implementation plan, version index)
- [ ] Code reviewed and approved (if PR process used)
- [ ] Deployed to production (via CI/CD)
- [ ] No critical bugs reported within 24 hours
- [ ] App starts successfully when S3 unavailable (core feature)
- [ ] App starts successfully when S3 available (no regression)
- [ ] Logs show appropriate messages for both S3 success and fallback scenarios

## Rollback Procedure

1. Identify issue (app crash, unexpected behavior, errors in logs)
2. Revert commit using git: `git revert <commit-hash>`
3. Push revert commit to trigger CI/CD
4. Verify v2.0.0 deployed successfully
5. Check S3 files exist in production bucket
6. Restart application services if needed
7. Monitor logs for normal S3 fetch messages
8. Verify app functionality restored

**Alternative Emergency Rollback:**
1. Checkout previous commit: `git checkout <v2.0.0-commit-hash>`
2. Force push to main (requires admin access): `git push --force origin main`
3. Trigger manual deployment if CI/CD doesn't auto-deploy
4. Document reason for force push in team communication

## Post-Deployment

### Monitoring

Monitor for 24-48 hours after deployment:
- Application startup errors (check container/process logs)
- S3 connection errors in logs
- Fallback file usage frequency (should be zero in production if S3 healthy)
- User reports of issues (settings not persisting, wrong prompts, etc.)

**Key metrics to watch:**
- Application uptime (should not decrease)
- Log volume of ERROR level messages (should not increase)
- Frequency of "Using fallback file" messages (indicates S3 issues)

**Alert conditions:**
- If "Using fallback file" appears in production logs (indicates S3 problem)
- If "FileNotFoundError" appears (indicates missing fallback files)
- If application restart frequency increases

### Follow-up Tasks

- [ ] Monitor logs for S3 errors in first week
- [ ] If fallback frequently used, investigate S3 reliability
- [ ] Consider adding health check endpoint that reports S3 vs fallback status
- [ ] Consider adding admin UI indicator showing config source (S3 vs fallback)
- [ ] Update runbook/playbook with troubleshooting steps for S3 issues
- [ ] (Optional) Add Prometheus metrics for config load success/fallback rate

---

**Generated**: 2025-12-28
**Author**: AI-assisted planning via /design command
**Version**: v2.0.1
