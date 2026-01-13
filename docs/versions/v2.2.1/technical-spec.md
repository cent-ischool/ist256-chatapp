# Technical Specification: Whitelist Refactoring & Bug Fixes - v2.2.1

## Overview

Version 2.2.1 refactors the roster/whitelist system to use centralized configuration instead of environment variables, renames "roster" terminology to "whitelist" for consistency throughout the codebase, and fixes bugs in the whitelist management page. This eliminates the need for the `ROSTER_FILE` environment variable and consolidates whitelist configuration in the `config.yaml` file stored in MinIO S3.

### Features Summary
- **Configuration Consolidation** - Whitelist filename comes from `config.whitelist` instead of `ROSTER_FILE` env var
- **Terminology Consistency** - Rename all "roster" references to "whitelist" across the codebase
- **File Renaming** - Rename `roster.py` to `whitelist.py` for consistency
- **UI Improvements** - Display whitelist filename from config in the admin page
- **Bug Fixes** - Address any issues in the whitelist management page

## Architecture Changes

### Components Affected

| File | Change Type | Description |
|------|-------------|-------------|
| [/workspaces/ist256-chatapp/app/dal/models.py](../../app/dal/models.py) | No change | `AppSettingsModel.whitelist` field already exists (line 32) |
| [/workspaces/ist256-chatapp/app/chat/app.py](../../app/chat/app.py) | Modify | Change `os.environ["ROSTER_FILE"]` to `st.session_state.config.whitelist` (line 133) |
| [/workspaces/ist256-chatapp/app/chat/session.py](../../app/chat/session.py) | Modify | Update whitelist loading to use config, rename Roster to Whitelist (lines 23, 57-58) |
| [/workspaces/ist256-chatapp/app/chat/roster.py](../../app/chat/roster.py) | Delete | To be renamed to whitelist.py |
| [/workspaces/ist256-chatapp/app/dal/s3.py](../../app/dal/s3.py) | Modify | Rename `put_roster()` to `put_whitelist()`, update docs (lines 96-113) |
| [/workspaces/ist256-chatapp/app/utils.py](../../app/utils.py) | Modify | Update example code using `ROSTER_FILE` (line 199) |
| [/workspaces/ist256-chatapp/app/chat/constants.py](../../app/chat/constants.py) | Modify | Update VERSION to "2.2.1" (line 1) |
| [/workspaces/ist256-chatapp/CLAUDE.md](../../CLAUDE.md) | Modify | Update documentation to remove `ROSTER_FILE`, add `config.whitelist` |

### New Components

| File | Purpose |
|------|---------|
| [/workspaces/ist256-chatapp/app/chat/whitelist.py](../../app/chat/whitelist.py) | Renamed from roster.py - admin page for whitelist management with config-aware filename display |

### Dependencies

No new external dependencies required. Uses existing:
- `streamlit` for UI components
- `minio` for S3 operations (via S3Client)
- `loguru` for logging
- `pydantic` / `SQLModel` for data models

## Data Models

### Database Changes

**No database schema changes** - Whitelist data continues to be stored in MinIO S3 as a text file.

### API Changes

**S3Client class** ([app/dal/s3.py](../../app/dal/s3.py)):

**Method renaming:**
```python
# Before (v2.2.0):
def put_roster(self, bucket_name: str, object_key: str, emails: List[str]) -> None:

# After (v2.2.1):
def put_whitelist(self, bucket_name: str, object_key: str, emails: List[str]) -> None:
```

Function signature remains the same, only the name changes for consistency.

**AppSettingsModel** ([app/dal/models.py](../../app/dal/models.py)):

No changes needed - `whitelist` field already exists (line 32):
```python
class AppSettingsModel(BaseModel):
    whitelist: str = ""  # Stores whitelist filename (e.g., "ist256-fall2025-roster.txt")
```

## Technical Design

### Backend Implementation

#### 1. S3Client Method Renaming ([app/dal/s3.py](../../app/dal/s3.py))

Rename `put_roster()` to `put_whitelist()` (lines 96-113):

```python
def put_whitelist(self, bucket_name: str, object_key: str, emails: List[str]) -> None:
    """
    Upload whitelist file (comma-separated emails) to S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (whitelist file name)
        emails: List of email addresses

    Returns:
        None
    """
    # Join emails with commas (matching format of get_roster)
    content = ",".join(emails)

    # Use existing put_text_file method
    self.put_text_file(bucket_name, object_key, content)
    logger.info(f"Uploaded whitelist to s3://{bucket_name}/{object_key}, email_count={len(emails)}")
```

**Note:** `get_roster()` function (lines 117-140) is a legacy standalone function and will remain unchanged to avoid breaking backward compatibility. Only the S3Client method is renamed.

#### 2. Configuration-Based Whitelist Loading

Replace all `os.environ["ROSTER_FILE"]` references with `st.session_state.config.whitelist` or pass config as parameter.

**Key files to update:**
- **app.py** (line 133): Authorization check
- **session.py** (lines 23, 58): Display whitelist users
- **whitelist.py** (lines 24, 85, display name): Load/save whitelist

**Design pattern:**
```python
# Before (v2.2.0):
whitelist_file = os.environ["ROSTER_FILE"]

# After (v2.2.1):
whitelist_file = st.session_state.config.whitelist
```

#### 3. Whitelist Admin Page ([app/chat/whitelist.py](../../app/chat/whitelist.py))

Rename `roster.py` to `whitelist.py` and update:

**Key changes:**
1. Function name: `show_roster()` → `show_whitelist()`
2. Page title: "Roster Management" → "Whitelist Management"
3. Variable names: `roster` → `whitelist`, `emails` → `emails`
4. Use `st.session_state.config.whitelist` instead of `os.environ["ROSTER_FILE"]`
5. Display whitelist filename from config in page header
6. Update all log messages to say "whitelist" instead of "roster"
7. Update S3Client method call: `put_roster()` → `put_whitelist()`

**New display section:**
```python
st.title("Whitelist Management")
st.markdown(f"Manage the whitelist of authorized users.")
st.info(f"📄 Current whitelist file: `{st.session_state.config.whitelist}`")
```

### Frontend Implementation

#### Admin Menu Update ([app/chat/app.py](../../app/chat/app.py))

Update admin menu option (line 162):
```python
# Before:
options=["Chat", "Settings", "Export", "Roster", "Session"]

# After:
options=["Chat", "Settings", "Export", "Whitelist", "Session"]
```

#### Page Routing ([app/chat/app.py](../../app/chat/app.py))

Update routing (lines 324-331):
```python
# Before:
elif current_page == "Roster":
    try:
        import roster
        roster.show_roster()
        logger.info(f"Admin user {st.session_state.auth_model.email} navigated to Roster")
    except Exception as e:
        st.error("Unable to load Roster page...")
        logger.error(f"Failed to load Roster page: user={st.session_state.auth_model.email}, error={e}", exc_info=True)

# After:
elif current_page == "Whitelist":
    try:
        import whitelist
        whitelist.show_whitelist()
        logger.info(f"Admin user {st.session_state.auth_model.email} navigated to Whitelist")
    except Exception as e:
        st.error("Unable to load Whitelist page...")
        logger.error(f"Failed to load Whitelist page: user={st.session_state.auth_model.email}, error={e}", exc_info=True)
```

#### Session Page Update ([app/chat/session.py](../../app/chat/session.py))

Update terminology and configuration source (lines 17-24, 57-70):
```python
# Load whitelist from config instead of env var
try:
    whitelist_file = st.session_state.config.whitelist if 'config' in st.session_state else os.environ.get("ROSTER_FILE", "roster.txt")
    whitelist_users = [user.lower().strip() for user in get_roster(
        os.environ["S3_HOST"],
        os.environ["S3_ACCESS_KEY"],
        os.environ["S3_SECRET_KEY"],
        os.environ["S3_BUCKET"],
        whitelist_file
    ) if user.strip()]
except Exception as e:
    st.error(f"Failed to load whitelist: {e}")
    whitelist_users = []

# Update expander section
with st.expander(f"📋 Whitelist Users ({len(whitelist_users)})", expanded=False):
    st.markdown(f"**Source:** `{whitelist_file}` in MinIO S3")
    st.markdown("**Access:** Standard chat access (no admin pages)")
```

### Integration Points

| Component | Integration |
|-----------|-------------|
| **MinIO S3** | Whitelist read via `get_roster()`, write via renamed `put_whitelist()` |
| **PostgreSQL** | No integration - whitelist is S3-based |
| **Configuration** | Whitelist filename stored in `AppSettingsModel.whitelist` field |
| **Session State** | Uses `st.session_state.config` for whitelist filename |
| **Environment Vars** | Removes dependency on `ROSTER_FILE` env var |

## Configuration

### Environment Variables

**Removed:**
- `ROSTER_FILE` - No longer needed, replaced by `config.whitelist`

**Still Required (unchanged):**
- `S3_HOST` - MinIO server address
- `S3_BUCKET` - Bucket containing whitelist file
- `S3_ACCESS_KEY` - MinIO access key
- `S3_SECRET_KEY` - MinIO secret key
- `CONFIG_FILE` - Configuration filename in S3 (default: "config.yaml")
- `ADMIN_USERS` - Comma-separated admin emails
- `ROSTER_EXCEPTION_USERS` - Comma-separated exception emails

### Config Files

**config.yaml structure** (stored in MinIO S3):
```yaml
configuration:
  ai_model: "gpt-4o-mini"
  temperature: 0.0
  answer_prompt: "Your name is Answerbot..."
  tutor_prompt: "Your name is Tutorbot..."
  whitelist: "ist256-fall2025-roster.txt"  # Whitelist filename
```

**Migration from v2.2.0:**
- If `whitelist` field is missing from config.yaml, `AppSettingsModel.from_yaml_string()` will use default empty string
- Application will gracefully handle missing field (existing behavior from v2.1.0)
- Admin can update whitelist filename via Settings page

**VERSION constant update** ([app/chat/constants.py](../../app/chat/constants.py)):
```python
VERSION="2.2.1"
```

## Security Considerations

| Consideration | Handling |
|---------------|----------|
| **Admin-only access** | Whitelist page restricted to admin users (same as v2.2.0) |
| **Configuration tampering** | Config stored in S3 (admin-writable), not exposed to non-admin users |
| **Backward compatibility** | Legacy `get_roster()` function unchanged, `ROSTER_FILE` env var still works as fallback |
| **Authorization** | Uses existing admin/exception/roster validation logic (unchanged) |
| **Audit trail** | All whitelist changes logged with admin email and timestamp |

**Security notes:**
- No new security risks introduced
- Configuration-based approach is more maintainable than env vars
- Fallback to env var ensures no breaking changes if config missing

## Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Configuration loading** | Whitelist filename loaded once per session (no performance impact) |
| **S3 operations** | No change in S3 call frequency (same as v2.2.0) |
| **Memory** | Negligible - one additional string field in session state |
| **Page load** | No impact - same whitelist loading mechanism |

**Optimizations:**
- Configuration loaded once at session init (cached in session state)
- No additional S3 calls beyond what v2.2.0 does

## Error Handling

### Expected Errors

| Error | Handling | User Message |
|-------|----------|--------------|
| **Config missing whitelist field** | Use empty string default | "Warning: Whitelist file not configured" |
| **Whitelist file not found in S3** | Catch exception, show error | "Failed to load whitelist: File not found" |
| **Config not loaded in session** | Fallback to env var if available | (Silent fallback for backward compatibility) |
| **S3 unavailable** | Catch exception, show error | "Failed to load whitelist from S3: {error}" |

### Logging

All operations logged with:
- Admin user email performing action
- Whitelist filename used
- Success/failure status
- Full exception traces on errors

Example log entries:
```
INFO: Admin user@syr.edu saved whitelist to ist256-fall2025-roster.txt with 247 emails
INFO: Loaded whitelist from config: ist256-fall2025-roster.txt
ERROR: Failed to load whitelist: File not found in S3
```

## Testing Strategy

### Unit Tests

| Test Case | Description |
|-----------|-------------|
| `test_put_whitelist_method` | S3Client.put_whitelist() works correctly |
| `test_whitelist_config_loading` | Whitelist filename loads from config |
| `test_whitelist_fallback` | Falls back to env var if config missing |
| `test_whitelist_page_display` | Whitelist filename displayed correctly in UI |

### Integration Tests

| Test Case | Description |
|-----------|-------------|
| **Whitelist page load** | Admin can access and see whitelist filename from config |
| **Whitelist save** | Edited whitelist persists to S3 using config filename |
| **Session page** | Correctly displays whitelist users with config-based filename |
| **Authorization** | Auth check uses config.whitelist correctly |
| **Config missing field** | Graceful handling when whitelist field absent |

### Manual Testing Checklist

#### Whitelist Page Testing
- [ ] Page title shows "Whitelist Management" (not "Roster")
- [ ] Info banner shows current whitelist filename from config
- [ ] Can load and display emails from config-based filename
- [ ] Can save emails to config-based filename
- [ ] Success messages say "whitelist" (not "roster")
- [ ] Log messages say "whitelist" (not "roster")

#### Session Page Testing
- [ ] Section header says "Whitelist Users" (not "Roster Users")
- [ ] Source line shows correct filename from config
- [ ] Whitelist users load and display correctly
- [ ] Fallback to env var if config not loaded

#### Admin Menu Testing
- [ ] Menu option says "Whitelist" (not "Roster")
- [ ] Clicking "Whitelist" navigates to correct page
- [ ] Other admin pages still work

#### Configuration Testing
- [ ] Config with whitelist field loads correctly
- [ ] Config without whitelist field uses empty string default
- [ ] Can update whitelist filename via Settings page
- [ ] Updated filename used immediately in Whitelist page

#### Authorization Testing
- [ ] Authorization check uses config.whitelist filename
- [ ] Users on whitelist can login
- [ ] Users not on whitelist are denied (correct error message)
- [ ] Admin/exception users bypass whitelist check

#### Edge Cases
- [ ] Empty whitelist filename in config (handle gracefully)
- [ ] Whitelist file missing from S3 (error handling)
- [ ] Config not loaded in session (fallback behavior)
- [ ] Very long whitelist filename (UI displays correctly)
- [ ] Special characters in filename (handled correctly)

#### Terminology Audit
- [ ] No references to "roster" in UI text
- [ ] No references to "roster" in log messages
- [ ] Variable names use "whitelist" terminology
- [ ] Function names use "whitelist" terminology
- [ ] Documentation uses "whitelist" terminology

## Rollback Plan

1. **Revert code changes**
   - `git revert <v2.2.1-commit-hash>`
   - Whitelist file in S3 remains unchanged
   - `ROSTER_FILE` env var still works (backward compatible)

2. **No database rollback needed**
   - No schema changes made

3. **Configuration rollback**
   - Config.yaml in S3 unchanged (whitelist field is optional)
   - If whitelist filename was changed, restore via Settings page
   - Or manually edit config.yaml in S3

4. **Verification after rollback**
   - Admin menu shows "Roster" option (not "Whitelist")
   - roster.py file exists (whitelist.py removed)
   - `ROSTER_FILE` env var used again
   - Authorization still works

## References

- Requirements: [/workspaces/ist256-chatapp/docs/project_requirements.md](../../docs/project_requirements.md) (v2.2.1 section)
- App Settings Model: [/workspaces/ist256-chatapp/app/dal/models.py](../../app/dal/models.py) (whitelist field line 32)
- S3Client: [/workspaces/ist256-chatapp/app/dal/s3.py](../../app/dal/s3.py)
- Roster page (to be renamed): [/workspaces/ist256-chatapp/app/chat/roster.py](../../app/chat/roster.py)
- Session page: [/workspaces/ist256-chatapp/app/chat/session.py](../../app/chat/session.py)
- Main app: [/workspaces/ist256-chatapp/app/chat/app.py](../../app/chat/app.py)
- Previous version (v2.2.0): [/workspaces/ist256-chatapp/docs/versions/v2.2.0/](../v2.2.0/)

---

**Generated**: 2026-01-13
**Author**: AI-assisted design via /design command
**Version**: 2.2.1
