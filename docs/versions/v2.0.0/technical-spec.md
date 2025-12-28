# Technical Specification: Application Migration to Production - v2.0.0

## Overview

Version 2.0.0 represents the official production release of the refactored IST256 AI Tutor chatbot. This is a **breaking change** that completes the migration from the legacy `app.py` to the new `appnew.py` architecture that was developed incrementally through versions 1.0.2 through 1.0.10. The new application features a modernized UI with mode/context selection, persistent user preferences, comprehensive chat logging, always-on context injection, and admin export capabilities.

This version:
- Renames the legacy `app.py` to `app_v1.py` (preserved for reference)
- Renames `appnew.py` to `app.py` (becomes the main application)
- Updates deployment configuration (Docker Compose, VSCode launch.json)
- Disables Streamlit's email prompt on startup
- Updates all documentation to reflect the new standard
- Marks all v1.0.x versions as Released in project requirements

## Architecture Changes

### Components Affected

- [/workspaces/ist256-chatapp/app/chat/app.py](../../../app/chat/app.py)
  - Will be renamed from current legacy version to `app_v1.py`

- [/workspaces/ist256-chatapp/app/chat/appnew.py](../../../app/chat/appnew.py)
  - Will be renamed to `app.py` (main application entry point)

- [/workspaces/ist256-chatapp/docker-compose.yaml](../../../docker-compose.yaml)
  - Update entry point command to reference `app.py` instead of `appnew.py`
  - Add Streamlit configuration flags to disable email collection

- [/workspaces/ist256-chatapp/.vscode/launch.json](../../../.vscode/launch.json)
  - Update debugger configuration to target `app.py` instead of `appnew.py`

- [/workspaces/ist256-chatapp/CLAUDE.md](../../../CLAUDE.md)
  - Update all references from `appnew.py` to `app.py`
  - Update architecture documentation to reflect v2.0 as production
  - Remove references to v1 as legacy

- [/workspaces/ist256-chatapp/docs/project_requirements.md](../../../docs/project_requirements.md)
  - Mark v1.0.2 through v1.0.10 as "Released" status
  - Add release date (deployment date)
  - Mark v2.0.0 as "Released" after deployment

- [/workspaces/ist256-chatapp/README.md](../../../README.md)
  - Update getting started instructions if they reference old filenames
  - Update feature list to reflect v2.0 capabilities

- [/workspaces/ist256-chatapp/app/chat/constants.py](../../../app/chat/constants.py)
  - Update VERSION from "1.0.10" to "2.0.0"

### New Components

None. This version performs refactoring and deployment configuration only.

### Dependencies

**Prerequisites:**
- All versions v1.0.2 through v1.0.10 must be complete and tested
- `appnew.py` must have full feature parity with original `app.py` plus all new v2.0 features:
  - MSAL authentication (v1.0.2)
  - Database and ChatLogger integration (v1.0.3)
  - LLM API integration with mode selection (v1.0.4)
  - Always-on context injection (v1.0.5)
  - Chat logging (v1.0.6)
  - Admin menu with Settings, Prompts, Session pages (v1.0.7)
  - UI polish, help/about, error handling (v1.0.8)
  - Export logs feature (v1.0.9)
  - Persistent user preferences (v1.0.10)

**External Dependencies:**
- All existing dependencies from `requirements.txt` (no new libraries required)
- Streamlit >= 1.30 (for `--server.headless` and config flags)

## Data Models

### Database Changes

**No schema changes required.** All database models are already in place from prior versions:
- `LogModel` - Chat message logging (v1.0.3, v1.0.6)
- `UserPreferencesModel` - User preferences for mode/context (v1.0.10)

### API Changes

**No API changes.** This is a deployment/configuration release only.

## Technical Design

### Backend Implementation

No backend code changes required. The backend implementation is complete from v1.0.2 through v1.0.10.

**File Rename Operations:**
1. Rename existing `app.py` → `app_v1.py` (preserve for reference)
2. Rename `appnew.py` → `app.py` (becomes production application)

**Verification Steps:**
- Ensure `app.py` (formerly `appnew.py`) has all imports and functionality working
- Test authentication flow
- Test database connections
- Test LLM integration
- Test S3 config loading

### Frontend Implementation

**Streamlit Configuration Updates:**

The main change is configuring Streamlit to disable the email collection prompt that appears on first launch.

**Method 1: Command-line flags (recommended for Docker)**
```bash
streamlit run app.py \
  --server.headless true \
  --browser.gatherUsageStats false \
  --client.showErrorDetails false
```

**Method 2: Config file (optional)**
Create `.streamlit/config.toml`:
```toml
[server]
headless = true

[browser]
gatherUsageStats = false

[client]
showErrorDetails = false
```

**UI Components:**
- No new UI components required
- All UI is inherited from v1.0.2-v1.0.10 implementation

### Integration Points

**Docker Compose:**
- Update `command:` in `docker-compose.yaml` to launch `app.py` with proper flags
- Example:
  ```yaml
  command: >
    streamlit run app.py
    --server.headless true
    --browser.gatherUsageStats false
    --client.showErrorDetails false
  ```

**VSCode Debugging:**
- Update `.vscode/launch.json` to point to `app/chat/app.py` instead of `app/chat/appnew.py`
- Example:
  ```json
  {
    "name": "Streamlit: app.py",
    "type": "python",
    "request": "launch",
    "module": "streamlit",
    "args": [
      "run",
      "app/chat/app.py",
      "--server.headless",
      "true"
    ]
  }
  ```

**GitHub Actions CI/CD:**
- No changes required to `.github/workflows/build_and_publish.yaml`
- The Docker image build will automatically use the updated `docker-compose.yaml`

**MinIO S3:**
- No changes required
- Config files (`config.yaml`, `prompts.yaml`, roster files) remain unchanged

**PostgreSQL:**
- No changes required
- All tables and models already deployed from v1.0.3/v1.0.10

**Azure OpenAI / Ollama:**
- No changes required
- LLM integration complete from v1.0.4

## Configuration

### Environment Variables

**No new environment variables required.**

All existing environment variables remain the same:
- `LLM` - "azure" or "ollama"
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_VERSION`
- `OLLAMA_HOST`
- `DATABASE_URL`
- `MSAL_CLIENT_ID`
- `MSAL_AUTHORITY`
- `S3_HOST`
- `S3_BUCKET`
- `S3_ACCESS_KEY`
- `S3_SECRET_KEY`
- `LOCAL_FILE_CACHE`
- `CONFIG_FILE`
- `PROMPTS_FILE`
- `ROSTER_FILE`
- `ADMIN_USERS`
- `ROSTER_EXCEPTION_USERS`

### Config Files

**app/chat/constants.py:**
- Line 1: Change `VERSION="1.0.10"` to `VERSION="2.0.0"`

**docker-compose.yaml:**
- Update `command:` section to include Streamlit flags:
  ```yaml
  command: >
    streamlit run app.py
    --server.headless true
    --browser.gatherUsageStats false
    --client.showErrorDetails false
  ```
- Update any references from `appnew.py` to `app.py`

**.vscode/launch.json (if exists):**
- Update `args` array to reference `app/chat/app.py`
- Add Streamlit configuration flags

**No changes to:**
- `app/data/config.yaml` (template)
- `app/data/prompts.yaml` (template)
- MinIO S3 stored configs

## Security Considerations

### Authentication

- **No changes** - MSAL authentication remains from v1.0.2
- Admin, exception, and roster users continue to be validated

### Authorization/Access Control

- **No changes** - Admin menu access control remains from v1.0.7
- User type detection (admin, exception, roster) unchanged

### Data Privacy

- **Improvement**: Streamlit's email collection is disabled in v2.0.0
  - `--browser.gatherUsageStats false` prevents Streamlit from collecting analytics
  - This enhances student privacy

### Input Validation

- **No changes** - All input validation implemented in v1.0.4-v1.0.8

### SQL Injection Prevention

- **No changes** - Continues to use SQLModel/SQLAlchemy parameterized queries

### XSS Prevention

- **No changes** - Streamlit handles HTML escaping by default

## Performance Considerations

### Scalability

**No performance impact.** This is a rename/configuration change only.

### Caching

**No changes** - Existing Streamlit caching decorators remain:
- `@st.cache_resource` for S3 client, DB connection
- `@st.cache_data` for configuration loading

### Database Query Optimization

**No changes** - Existing query patterns from v1.0.3, v1.0.6, v1.0.10 remain.

### Memory Usage

**No changes** - Application memory footprint unchanged.

## Error Handling

### Expected Errors

**File Not Found Errors (during rename):**
- **Error**: "app.py already exists"
- **Handling**: Check if previous migration was partially completed
- **Resolution**: Manually inspect file contents and decide which to keep

**Docker Build Errors:**
- **Error**: "app.py not found" during Docker build
- **Handling**: Ensure rename operations completed before building image
- **Resolution**: Verify file exists at `/workspaces/ist256-chatapp/app/chat/app.py`

**Streamlit Configuration Errors:**
- **Error**: "Unknown flag: --server.headless"
- **Handling**: Streamlit version too old
- **Resolution**: Upgrade Streamlit to >= 1.30

### User-Facing Error Messages

**No new user-facing errors.** All error messages inherited from v1.0.2-v1.0.10.

### Logging Requirements

**No additional logging required.**

Existing logging continues:
- Chat messages logged to PostgreSQL (v1.0.6)
- User preferences logged to PostgreSQL (v1.0.10)

### Recovery Procedures

**Rollback to v1:**
1. Rename `app.py` → `appnew.py` (restore new app to development name)
2. Rename `app_v1.py` → `app.py` (restore legacy app to production)
3. Revert `docker-compose.yaml` changes
4. Revert `.vscode/launch.json` changes
5. Change VERSION back to "1.0.10" in constants.py
6. Rebuild Docker image

## Testing Strategy

### Unit Tests

**No unit tests required.** This is a configuration/rename release.

If unit tests exist in the project:
- Ensure test imports reference the correct file names
- Update any hardcoded paths from `appnew.py` to `app.py`

### Integration Tests

**Manual integration testing required:**

1. **File Rename Verification:**
   - [ ] Confirm `app_v1.py` exists and contains legacy code
   - [ ] Confirm `app.py` exists and contains new v2.0 code
   - [ ] Verify no broken imports in either file

2. **Local Development:**
   - [ ] Run `streamlit run app/chat/app.py`
   - [ ] Verify no Streamlit email prompt appears
   - [ ] Verify authentication flow works
   - [ ] Verify chat functionality works
   - [ ] Verify admin menu works

3. **Docker Build & Run:**
   - [ ] Build Docker image: `docker-compose build`
   - [ ] Run container: `docker-compose up`
   - [ ] Verify container starts without errors
   - [ ] Access application in browser
   - [ ] Verify no Streamlit email prompt
   - [ ] Test full user flow (login → select context → chat)

4. **VSCode Debugging:**
   - [ ] Launch debugger with updated configuration
   - [ ] Set breakpoint in `app.py`
   - [ ] Verify debugger attaches correctly

### Manual Testing

**Test Plan:**

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Application Launch | Run `streamlit run app.py --server.headless true` | App starts, no email prompt |
| Authentication | Login with valid user | User authenticated, redirected to chat |
| Mode Selection | Switch between Tutor/Answer modes | Mode persists, system prompt changes |
| Context Selection | Select assignment context | Context loads, greeting shows assignment name |
| Chat Interaction | Send user message | LLM responds, messages logged to database |
| User Preferences | Change mode/context, logout, login | Preferences loaded from database |
| Admin Access | Login as admin user | Admin menu visible in sidebar |
| Admin Export | Navigate to Export page | Can export logs as CSV/JSON |
| Admin Settings | Navigate to Settings page | Can modify AI model, temperature |
| Docker Deployment | Deploy via Docker Compose | Container runs successfully, all features work |

**User Types to Test:**
- [ ] Admin user (in ADMIN_USERS env var)
- [ ] Exception user (in ROSTER_EXCEPTION_USERS env var)
- [ ] Roster user (in roster file)
- [ ] Unauthorized user (not in any list)

**Edge Cases:**
- [ ] Empty roster file (should allow all users)
- [ ] Missing config.yaml in S3 (should use defaults from app/data/)
- [ ] Missing prompts.yaml in S3 (should use defaults from app/data/)
- [ ] Database connection failure (should show error message)
- [ ] S3 connection failure (should fall back to local defaults)

## Rollback Plan

### Immediate Rollback (Production Emergency)

If critical issues arise after deployment:

1. **Revert Git Commit:**
   ```bash
   git revert HEAD
   git push origin main
   ```

2. **Manual File Restoration (if needed):**
   ```bash
   mv app/chat/app.py app/chat/appnew.py
   mv app/chat/app_v1.py app/chat/app.py
   ```

3. **Rebuild Docker Image:**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

4. **Verify Rollback:**
   - Check application is accessible
   - Verify legacy UI is functioning
   - Confirm user can login and chat

### Database Rollback

**Not required.** No schema changes in v2.0.0.

The database is forward-compatible:
- LogModel remains unchanged
- UserPreferencesModel remains unchanged

If rolling back to v1 (legacy app):
- User preferences will not be used (v1 doesn't read them)
- Chat logs will continue to accumulate
- No data loss occurs

### Configuration Rollback

1. **docker-compose.yaml:**
   - Revert command to use `appnew.py`
   - Remove Streamlit flags (or keep them, they're harmless)

2. **.vscode/launch.json:**
   - Revert args to reference `appnew.py`

3. **constants.py:**
   - Revert VERSION to "1.0.10"

### Post-Rollback Communication

If rollback occurs:
1. Notify users via course announcement (IST256 Canvas/Blackboard)
2. Log issue in GitHub repository
3. Document root cause in post-mortem
4. Create hotfix branch to address issue
5. Re-deploy v2.0.0 after fix

## References

### Related Requirements
- [project_requirements.md v2.0.0 section](../../project_requirements.md#v200)

### Related Versions
- v1.0.2: Authentication & Authorization
- v1.0.3: Database & Logging Infrastructure
- v1.0.4: LLM Integration
- v1.0.5: Context Injection
- v1.0.6: Chat Logging
- v1.0.7: Admin Menu
- v1.0.8: UI Polish
- v1.0.9: Export Logs
- v1.0.10: Persistent User Preferences

### External Documentation
- [Streamlit Configuration Options](https://docs.streamlit.io/library/advanced-features/configuration)
- [Docker Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Semantic Versioning 2.0.0](https://semver.org/)

---

**Generated**: 2025-12-28
**Author**: AI-assisted design via /design command
**Version**: 2.0.0
