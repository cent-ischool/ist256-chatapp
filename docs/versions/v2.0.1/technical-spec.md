# Technical Specification: S3 Config Fallback Error Handling - v2.0.1

## Overview

This patch version adds robust error handling for S3 configuration file loading. Currently, if the app cannot read config.yaml or prompts.yaml from MinIO S3 (e.g., files not yet uploaded), the application crashes. This fix implements a graceful fallback mechanism that logs the S3 error and loads local fallback files from the filesystem, allowing the application to start successfully even when S3 is unavailable or files are missing.

## Architecture Changes

### Components Affected

- `/workspaces/ist256-chatapp/app/dal/s3.py` - S3Client class
  - Modify `get_text_file()` method signature to accept optional fallback file path
  - Add error handling logic to catch S3 exceptions
  - Add fallback file loading from local filesystem
  - Add logging for both S3 errors and successful fallback loads

### New Components

None - this is a modification to existing component only.

### Dependencies

- Existing: `loguru` (already in use for logging)
- Existing: `minio` (S3 client library)
- No new external dependencies required

## Data Models

### Database Changes

None - this feature does not affect database schema.

### API Changes

**Modified Method Signature:**

```python
# Current signature:
def get_text_file(self, bucket_name: str, object_key: str) -> str:

# New signature:
def get_text_file(self, bucket_name: str, object_key: str, fallback_file_path: str = None) -> str:
```

**Parameters:**
- `bucket_name` (str): S3 bucket name
- `object_key` (str): S3 object key (file path in bucket)
- `fallback_file_path` (str, optional): Local filesystem path to fallback file. If S3 load fails and this is provided, load from local file. If not provided, raise the original exception.

**Return:**
- `str`: File content as UTF-8 string

**Behavior:**
1. Attempt to fetch from S3 (existing behavior)
2. If S3 fetch fails and `fallback_file_path` is provided:
   - Log error with S3 details
   - Load from local fallback file
   - Log successful fallback load
   - Return fallback content
3. If S3 fetch fails and no fallback provided:
   - Raise original exception (existing behavior)

## Technical Design

### Backend Implementation

**Algorithm for `get_text_file()` modification:**

```python
def get_text_file(self, bucket_name: str, object_key: str, fallback_file_path: str = None) -> str:
    try:
        # Existing S3 fetch logic
        response = self.client.get_object(bucket_name, object_key)
        file_content = response.read().decode('utf-8')
        logger.info(f"Fetched text file s3://{bucket_name}/{object_key}, size={len(file_content)} characters")
        return file_content
    except Exception as e:
        # New error handling
        if fallback_file_path:
            logger.error(f"Failed to fetch s3://{bucket_name}/{object_key}: {e}")
            logger.info(f"Using fallback file: {fallback_file_path}")
            with open(fallback_file_path, 'r', encoding='utf-8') as f:
                fallback_content = f.read()
            logger.info(f"Loaded fallback file {fallback_file_path}, size={len(fallback_content)} characters")
            return fallback_content
        else:
            # No fallback provided, re-raise original exception
            logger.error(f"Failed to fetch s3://{bucket_name}/{object_key} and no fallback provided: {e}")
            raise
```

**Error Handling:**
- Catch all exceptions from `self.client.get_object()` (network errors, auth failures, file not found, etc.)
- Use loguru logger for error and info messages
- Preserve existing behavior when no fallback provided (raise exception)

**File Loading:**
- Use standard Python `open()` with UTF-8 encoding for fallback files
- Close file properly using context manager (`with` statement)
- Validate fallback file exists (let `FileNotFoundError` propagate if missing)

### Frontend Implementation

No frontend changes required. This is purely a backend data access layer enhancement.

### Integration Points

**MinIO S3 Integration:**
- Uses existing Minio client instance
- Catches exceptions from `get_object()` method
- Logs S3-specific error details

**Filesystem Integration:**
- Reads from local filesystem using absolute or relative paths
- Expected fallback files location: `/workspaces/ist256-chatapp/app/data/`
- Falls back to local copies of config.yaml and prompts.yaml

**Application Integration:**
- Call sites in `app/chat/app.py` (lines 236-237) updated to pass fallback paths
- Call sites in `app/chat/settings.py` (lines 16-17) updated to pass fallback paths
- Call sites in `app/chat/prompts.py` (line 17) updated to pass fallback path

## Configuration

### Environment Variables

**New (Optional):**
- `CONFIG_FILE_FALLBACK` - Local fallback path for config.yaml (default: `app/data/config.yaml`)
- `PROMPTS_FILE_FALLBACK` - Local fallback path for prompts.yaml (default: `app/data/prompts.yaml`)

**Note:** These environment variables are optional. If not set, hardcoded relative paths can be used.

### Config Files

No changes to config.yaml or prompts.yaml structure. The fallback files in `/workspaces/ist256-chatapp/app/data/` will serve as templates and emergency fallbacks.

## Security Considerations

**Authentication:**
- No authentication changes
- S3 credentials still required (may fail gracefully now)

**Authorization/Access Control:**
- No authorization changes
- Fallback files should have appropriate filesystem permissions (readable by app process)

**Data Privacy:**
- No sensitive data in config.yaml or prompts.yaml (system prompts and model settings only)
- Fallback files stored in codebase, should not contain secrets

**Input Validation:**
- Validate fallback_file_path is a string if provided
- Let Python's `open()` validate file path (raises FileNotFoundError if invalid)
- No path traversal risk (internal config files only)

**Injection Prevention:**
- No SQL involved (file I/O only)
- No user input in file paths (hardcoded/env var only)
- YAML parsing happens at calling code level (no changes)

## Performance Considerations

**Scalability:**
- Minimal impact - fallback only triggered on S3 failure
- Local file I/O is faster than S3 fetch (actually improves startup time if S3 unavailable)

**Caching:**
- No caching changes - files loaded once at app initialization
- Fallback files cached in filesystem by OS

**Memory Usage:**
- Negligible - config files are small (< 1KB each)

**Error Recovery:**
- Graceful degradation: app can start with local config even if S3 down
- Reduces dependency on external service availability

## Error Handling

### Expected Errors

1. **S3 Connection Failure:**
   - Error: Network timeout, DNS failure, S3 host unreachable
   - Handling: Log error, load fallback file
   - User Message: None (transparent fallback)

2. **S3 File Not Found:**
   - Error: `NoSuchKey` exception from Minio
   - Handling: Log error, load fallback file
   - User Message: None (transparent fallback)

3. **S3 Authentication Failure:**
   - Error: `AccessDenied` exception from Minio
   - Handling: Log error, load fallback file
   - User Message: None (transparent fallback)

4. **Fallback File Not Found:**
   - Error: `FileNotFoundError` from Python open()
   - Handling: Raise exception (app cannot start)
   - User Message: Admin sees traceback in logs/console

5. **Fallback File Read Error:**
   - Error: Permission denied, disk error
   - Handling: Raise exception (app cannot start)
   - User Message: Admin sees traceback in logs/console

### Logging Requirements

**Log Levels:**
- `logger.error()` - S3 fetch failures
- `logger.info()` - Fallback file usage
- `logger.info()` - Successful fallback file load

**Log Messages:**
```
ERROR: Failed to fetch s3://bucket/config.yaml: [exception details]
INFO: Using fallback file: app/data/config.yaml
INFO: Loaded fallback file app/data/config.yaml, size=256 characters
```

### Recovery Procedures

1. If S3 down temporarily: App continues with fallback files, admin can upload to S3 later
2. If S3 files deleted: App continues with fallback files, admin re-uploads from local copies
3. If fallback files missing: App crashes at startup, admin restores fallback files from git

## Testing Strategy

### Unit Tests

Currently no test suite exists. If tests are added in future, test cases would include:

1. **Test S3 success path (existing behavior):**
   - Mock Minio client to return sample YAML content
   - Assert `get_text_file()` returns S3 content
   - Assert no fallback file accessed

2. **Test S3 failure with fallback:**
   - Mock Minio client to raise exception
   - Create temporary fallback file
   - Assert `get_text_file()` returns fallback content
   - Assert error logged

3. **Test S3 failure without fallback:**
   - Mock Minio client to raise exception
   - Do not provide fallback_file_path
   - Assert exception is raised

4. **Test fallback file not found:**
   - Mock Minio client to raise exception
   - Provide non-existent fallback path
   - Assert `FileNotFoundError` is raised

### Integration Tests

No automated integration tests exist. Manual testing procedures below.

### Manual Testing

**Test Case 1: Normal S3 Operation**
- Setup: S3 files exist and are accessible
- Steps:
  1. Start application normally
  2. Check logs for "Fetched text file s3://..."
  3. Verify app loads successfully
- Expected: No fallback used, S3 files loaded

**Test Case 2: S3 Files Missing**
- Setup: Temporarily rename files in S3 bucket
- Steps:
  1. Start application
  2. Check logs for "Failed to fetch" and "Using fallback file"
  3. Verify app loads successfully
  4. Check settings page shows default config values
- Expected: Fallback files loaded, app functional

**Test Case 3: S3 Service Unavailable**
- Setup: Change S3_HOST env var to invalid host
- Steps:
  1. Start application
  2. Check logs for connection error and fallback usage
  3. Verify app loads successfully
- Expected: Fallback files loaded after timeout

**Test Case 4: Fallback Files Missing**
- Setup: Temporarily rename `/workspaces/ist256-chatapp/app/data/config.yaml`
- Steps:
  1. Stop S3 or remove S3 files
  2. Start application
  3. Observe traceback/error
- Expected: App crashes with FileNotFoundError (cannot start)

**Test Case 5: Admin Settings Page**
- Setup: S3 operational
- Steps:
  1. Login as admin user
  2. Navigate to Settings page
  3. Modify configuration
  4. Save to S3
  5. Restart app
- Expected: S3 files loaded (not fallback), modified settings persist

**Test Case 6: Non-Admin User**
- Setup: S3 using fallback or not
- Steps:
  1. Login as non-admin roster user
  2. Use chat functionality
  3. Check that mode/context selection works
- Expected: No difference in user experience regardless of S3 vs fallback

## Rollback Plan

1. **If issues arise after deployment:**
   - Revert commit (git revert)
   - Redeploy previous version (v2.0.0)
   - No database changes to rollback (none made)
   - No config file format changes (backward compatible)

2. **Verification after rollback:**
   - Ensure S3 files are present in bucket
   - Verify app starts successfully with S3 files
   - Check logs for normal S3 fetch messages

3. **Emergency fix if rollback needed:**
   - If S3 files missing, manually upload from `/workspaces/ist256-chatapp/app/data/` to S3
   - Use MinIO web console or `s3cmd` CLI tool
   - Restart application

## References

- Related issue: App crashes when S3 config files unavailable
- Current S3 implementation: [s3.py:33-37](/workspaces/ist256-chatapp/app/dal/s3.py#L33-L37)
- App initialization: [app.py:236-237](/workspaces/ist256-chatapp/app/chat/app.py#L236-L237)
- MinIO documentation: https://min.io/docs/minio/linux/developers/python/API.html

---

**Generated**: 2025-12-28
**Author**: AI-assisted design via /design command
**Version**: v2.0.1
