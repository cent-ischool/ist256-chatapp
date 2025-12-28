# Implementation Plan: Application Migration to Production - v2.0.0

## Timeline

- **Estimated effort**: 2-3 hours
- **Complexity**: Low
- **Suggested sprint**: Single sprint (can be completed in one session)

## Phase 1: Preparation

### Tasks

- [ ] Review technical specification at `/workspaces/ist256-chatapp/docs/versions/v2.0.0/technical-spec.md`
- [ ] Verify all prerequisite versions (v1.0.2 through v1.0.10) are complete and tested
- [ ] Set up development branch: `feature/v2.0.0-production-migration`
- [ ] Create backup of current `app.py` (legacy version) to safe location
- [ ] Verify `appnew.py` has full feature parity and is production-ready
- [ ] Update TODO.txt with v2.0.0 migration tasks
- [ ] Review deployment pipeline (GitHub Actions, Docker Compose)

### Prerequisites

**Required Completions:**
- v1.0.2: MSAL authentication working in `appnew.py`
- v1.0.3: Database and ChatLogger initialized
- v1.0.4: LLM API integration functional
- v1.0.5: Context injection working with all assignments
- v1.0.6: Chat logging to PostgreSQL active
- v1.0.7: Admin menu accessible (Settings, Prompts, Session pages)
- v1.0.8: UI polish, help text, error handling complete
- v1.0.9: Export logs feature functional for admins
- v1.0.10: User preferences persisting to database

**Testing Verification:**
- [ ] Confirm `appnew.py` runs locally without errors
- [ ] Confirm authentication flow works (admin, exception, roster users)
- [ ] Confirm LLM responses are streaming correctly
- [ ] Confirm context injection loads assignment content
- [ ] Confirm chat logging writes to database
- [ ] Confirm admin export generates CSV/JSON files
- [ ] Confirm user preferences persist across sessions

**Environment Check:**
- [ ] All environment variables set in `.env` file
- [ ] PostgreSQL database accessible and tables created
- [ ] MinIO S3 accessible with config files
- [ ] Streamlit version >= 1.30 (for headless mode)
- [ ] Docker and Docker Compose installed (for deployment testing)

## Phase 2: File Renaming

### Tasks

- [ ] Rename `app/chat/app.py` → `app/chat/app_v1.py` (preserve legacy)
- [ ] Rename `app/chat/appnew.py` → `app/chat/app.py` (promote to production)
- [ ] Verify imports in `app.py` (formerly `appnew.py`) are correct
- [ ] Verify no broken relative imports
- [ ] Test that `app.py` runs locally: `streamlit run app/chat/app.py`

### Files to Modify

**Rename Operations (use `git mv` to preserve history):**

1. **Preserve Legacy Application:**
   ```bash
   git mv app/chat/app.py app/chat/app_v1.py
   ```
   - **Purpose**: Keep legacy app for reference and emergency rollback
   - **Validation**: Ensure file exists and contains v1 code

2. **Promote New Application to Production:**
   ```bash
   git mv app/chat/appnew.py app/chat/app.py
   ```
   - **Purpose**: Make new v2.0 app the main entry point
   - **Validation**: Ensure file exists and contains all v1.0.2-v1.0.10 features

### Files to Create

None. This phase only performs rename operations.

## Phase 3: Update Deployment Configuration

### Tasks

- [ ] Update `docker-compose.yaml` to reference `app.py` and add Streamlit flags
- [ ] Update `.vscode/launch.json` to reference `app.py` (if file exists)
- [ ] Test Docker build locally: `docker-compose build`
- [ ] Test Docker run locally: `docker-compose up`
- [ ] Verify container starts and application is accessible at `http://localhost:PORT`

### Files to Modify

1. **`/workspaces/ist256-chatapp/docker-compose.yaml`**
   - **Current command** (approximate):
     ```yaml
     command: streamlit run app/chat/appnew.py
     ```
   - **New command**:
     ```yaml
     command: >
       streamlit run app/chat/app.py
       --server.headless true
       --browser.gatherUsageStats false
       --client.showErrorDetails false
     ```
   - **Lines**: Find `command:` key in the service definition (typically lines 15-20)
   - **Reason**:
     - Update entry point to new `app.py` filename
     - Add `--server.headless true` to disable email collection prompt
     - Add `--browser.gatherUsageStats false` for privacy
     - Add `--client.showErrorDetails false` to suppress technical errors to end users

2. **`/workspaces/ist256-chatapp/.vscode/launch.json`** (if exists)
   - **Current configuration** (approximate):
     ```json
     {
       "name": "Streamlit Debug",
       "type": "python",
       "request": "launch",
       "module": "streamlit",
       "args": ["run", "app/chat/appnew.py"]
     }
     ```
   - **New configuration**:
     ```json
     {
       "name": "Streamlit Debug",
       "type": "python",
       "request": "launch",
       "module": "streamlit",
       "args": [
         "run",
         "app/chat/app.py",
         "--server.headless",
         "true",
         "--browser.gatherUsageStats",
         "false"
       ]
     }
     ```
   - **Lines**: Find the configuration for Streamlit debugging
   - **Reason**: Enable debugging of the new `app.py` file with proper flags

### Files to Create

**Optional: Create `.streamlit/config.toml`** (alternative to command-line flags)
- **Path**: `/workspaces/ist256-chatapp/.streamlit/config.toml`
- **Purpose**: Centralized Streamlit configuration
- **Content**:
  ```toml
  [server]
  headless = true
  port = 8501

  [browser]
  gatherUsageStats = false

  [client]
  showErrorDetails = false
  ```
- **Note**: This is optional. Command-line flags in docker-compose.yaml are sufficient.

## Phase 4: Update Version and Documentation

### Tasks

- [ ] Update VERSION constant in `app/chat/constants.py` to "2.0.0"
- [ ] Update `CLAUDE.md` to replace `appnew.py` references with `app.py`
- [ ] Update `CLAUDE.md` to document v2.0 as production architecture
- [ ] Update `README.md` if it contains file references or outdated architecture info
- [ ] Update `docs/project_requirements.md` to mark v1.0.2-v1.0.10 as Released
- [ ] Update `docs/versions/README.md` to add v2.0.0 entry

### Files to Modify

1. **`/workspaces/ist256-chatapp/app/chat/constants.py`**
   - **Line 1**: Change `VERSION="1.0.10"` to `VERSION="2.0.0"`
   - **Reason**: Reflect major version bump for breaking changes

2. **`/workspaces/ist256-chatapp/CLAUDE.md`**
   - **Changes**:
     - Find all instances of `appnew.py` and replace with `app.py`
     - Update "Architecture" section to describe v2.0 as the production architecture
     - Update "Important Files" section to reference `app.py` instead of `appnew.py`
     - Update "Chat Flow" section if it mentions `appnew.py`
   - **Estimated locations**: Lines 20-50, 100-150 (search for "appnew")
   - **Reason**: Keep developer documentation accurate

3. **`/workspaces/ist256-chatapp/docs/project_requirements.md`**
   - **Changes**:
     - For versions v1.0.2 through v1.0.10:
       - Change `**Status**: Planned` or `**Status**: In Development` to `**Status**: Released`
       - Update `**Release Date**: TBD` to actual release date (e.g., `2025-12-28`)
     - For version v2.0.0:
       - Change `**Status**: Planned` to `**Status**: Released` (after deployment)
       - Update `**Release Date**: TBD` to deployment date
   - **Lines**: Lines 33-271 (entire v1.0.2-v2.0.0 sections)
   - **Reason**: Maintain accurate version history

4. **`/workspaces/ist256-chatapp/docs/versions/README.md`**
   - **Changes**:
     - Add new row to version history table (at the top):
       ```markdown
       | v2.0.0 | TBD | In Development | Production release: rename appnew.py to app.py, update deployment config |
       ```
     - Insert as first row (latest version on top)
   - **Lines**: Around line 8-10 (version history table)
   - **Reason**: Track v2.0.0 in version index

5. **`/workspaces/ist256-chatapp/README.md`** (if exists and contains file references)
   - **Changes**:
     - Replace any references to `appnew.py` with `app.py`
     - Update "Getting Started" section if it shows how to run the app
     - Update feature list to reflect v2.0 capabilities (mode/context selection, user preferences, admin export)
   - **Reason**: Accurate user-facing documentation

### Configuration Changes

None. All configuration is in deployment files (docker-compose.yaml, launch.json).

## Phase 5: Testing

### Tasks

#### Local Testing

- [ ] **Run application locally**
  ```bash
  streamlit run app/chat/app.py --server.headless true
  ```
  - [ ] Verify app starts without errors
  - [ ] Verify no Streamlit email prompt appears
  - [ ] Verify UI loads correctly

- [ ] **Authentication Testing**
  - [ ] Test admin user login (should see admin menu)
  - [ ] Test exception user login (should access chat, no admin menu)
  - [ ] Test roster user login (should access chat, no admin menu)
  - [ ] Test unauthorized user (should see unauthorized message)

- [ ] **Mode and Context Testing**
  - [ ] Switch between Tutor and Answer modes
  - [ ] Verify system prompt changes (check LLM response style)
  - [ ] Select different assignment contexts (Lab-01, HW-02, etc.)
  - [ ] Verify assignment content is injected (ask assignment-specific question)
  - [ ] Switch context and verify chat history clears

- [ ] **Chat Functionality**
  - [ ] Send user message
  - [ ] Verify LLM streams response
  - [ ] Verify response appears in chat
  - [ ] Send follow-up message
  - [ ] Verify conversation history is maintained

- [ ] **User Preferences**
  - [ ] Change mode and context
  - [ ] Click "Save + New Chat"
  - [ ] Logout and login again
  - [ ] Verify mode and context are restored from database

- [ ] **Admin Features** (admin user only)
  - [ ] Navigate to Settings page
  - [ ] Modify AI model, temperature
  - [ ] Save settings
  - [ ] Verify settings persist in MinIO S3
  - [ ] Navigate to Prompts page
  - [ ] Edit system prompt
  - [ ] Save prompt
  - [ ] Verify prompt persists in MinIO S3
  - [ ] Navigate to Export page
  - [ ] Export logs as CSV
  - [ ] Verify file downloads
  - [ ] Export logs as JSON
  - [ ] Verify file downloads and format is correct
  - [ ] Navigate to Session page
  - [ ] Verify session state variables are displayed

- [ ] **Download Chat History** (all users)
  - [ ] Have a conversation with 3-5 messages
  - [ ] Expand "AI Mode/Context" section at bottom
  - [ ] Click "Download Chat" button
  - [ ] Verify Markdown file downloads with current session
  - [ ] Click "Download All" button
  - [ ] Verify Markdown file downloads with all user's sessions

#### Docker Testing

- [ ] **Build Docker Image**
  ```bash
  docker-compose build
  ```
  - [ ] Verify build completes without errors
  - [ ] Check for any deprecation warnings

- [ ] **Run Docker Container**
  ```bash
  docker-compose up
  ```
  - [ ] Verify container starts
  - [ ] Verify logs show "You can now view your Streamlit app in your browser"
  - [ ] Verify no error messages in logs

- [ ] **Access Dockerized Application**
  - [ ] Open browser to `http://localhost:<PORT>` (check docker-compose.yaml for port)
  - [ ] Verify app loads
  - [ ] Verify no Streamlit email prompt
  - [ ] Login and perform basic chat test

- [ ] **Environment Variable Validation**
  - [ ] Verify database connection works (chat logs are written)
  - [ ] Verify S3 connection works (config loads)
  - [ ] Verify LLM connection works (responses are generated)
  - [ ] Verify authentication works (MSAL redirects)

#### Edge Case Testing

- [ ] **Empty Roster File**
  - [ ] Temporarily set `ROSTER_FILE` to an empty file
  - [ ] Attempt login
  - [ ] Verify all users are allowed (empty roster = allow all)
  - [ ] Restore actual roster file

- [ ] **Missing Config in S3**
  - [ ] Temporarily remove `config.yaml` from MinIO S3
  - [ ] Restart application
  - [ ] Verify app uses defaults from `app/data/config.yaml`
  - [ ] Restore `config.yaml` to S3

- [ ] **Database Connection Failure**
  - [ ] Temporarily set `DATABASE_URL` to invalid connection string
  - [ ] Restart application
  - [ ] Verify error message is shown to user
  - [ ] Restore correct `DATABASE_URL`

- [ ] **S3 Connection Failure**
  - [ ] Temporarily set `S3_HOST` to invalid host
  - [ ] Restart application
  - [ ] Verify app falls back to local config files
  - [ ] Restore correct `S3_HOST`

- [ ] **LLM API Failure**
  - [ ] Temporarily set `AZURE_OPENAI_API_KEY` to invalid key
  - [ ] Send chat message
  - [ ] Verify error message is shown to user
  - [ ] Restore correct API key

### Test Data

**Test Users:**
- Admin: `mafudge@syr.edu` (or value in `ADMIN_USERS`)
- Exception: User email in `ROSTER_EXCEPTION_USERS`
- Roster: User email in roster file
- Unauthorized: Any email NOT in above lists

**Test Contexts:**
- General Python (no context)
- Lab-01-Intro
- HW-03-Conditionals
- Lab-12-WebAPIs (or any other available assignment)

**Test Prompts:**
- "Hello, what can you help me with?" (general greeting)
- "How do I create a for loop in Python?" (general Python question)
- "What is the goal of this assignment?" (context-specific question, requires context injection)
- "Can you solve problem 1 for me?" (tests Answer mode vs Tutor mode behavior)

## Phase 6: Documentation

### Tasks

- [ ] Review all changes to `CLAUDE.md` for accuracy
- [ ] Review all changes to `README.md` for clarity
- [ ] Verify inline code comments in `app.py` are sufficient
- [ ] Document any deployment issues encountered and solutions
- [ ] Update `docs/versions/README.md` with final release date for v2.0.0
- [ ] Create summary comment for commit message

### Documentation Files

- [x] `CLAUDE.md` - Developer guide (update `appnew.py` references)
- [ ] `README.md` - User-facing documentation (if applicable)
- [x] `docs/project_requirements.md` - Mark versions as Released
- [x] `docs/versions/README.md` - Add v2.0.0 to version index
- [x] `docs/versions/v2.0.0/technical-spec.md` - Technical specification (already created)
- [x] `docs/versions/v2.0.0/implementation-plan.md` - This document

### Inline Documentation

**Code Comments to Add (if not present):**

In `/workspaces/ist256-chatapp/app/chat/app.py` (top of file):
```python
# IST256 AI Tutor Chatbot - v2.0.0
# Main application entry point
# This file was previously named appnew.py and promoted to production in v2.0.0
# For legacy v1 code, see app_v1.py
```

In `/workspaces/ist256-chatapp/app/chat/app_v1.py` (top of file):
```python
# IST256 AI Tutor Chatbot - Legacy v1
# This file was the original app.py before v2.0.0
# Preserved for reference and emergency rollback
# DO NOT USE IN PRODUCTION - see app.py for current version
```

## Phase 7: Deployment

### Tasks

- [ ] Review all changes in git diff
- [ ] Verify VERSION is "2.0.0" in constants.py
- [ ] Verify all tests passed (Phase 5)
- [ ] Verify all documentation updated (Phase 6)
- [ ] Stage all changes: `git add .`
- [ ] Commit with standardized message (see below)
- [ ] Push feature branch to remote: `git push origin feature/v2.0.0-production-migration`
- [ ] Create pull request to `main` branch
- [ ] Request code review from team/instructor
- [ ] Address any review feedback
- [ ] Merge PR to `main` after approval
- [ ] Monitor GitHub Actions CI/CD pipeline
- [ ] Verify Docker image is built and pushed to registry
- [ ] Verify deployment to production environment succeeds
- [ ] Perform smoke test on production (login, send one message)
- [ ] Monitor error logs for first 24 hours

### Deployment Checklist

**Pre-Deployment:**
- [ ] All Phase 5 tests passing
- [ ] VERSION updated to "2.0.0"
- [ ] Documentation complete
- [ ] No merge conflicts with `main` branch
- [ ] Docker build successful locally
- [ ] All environment variables documented

**Commit Message Format:**
```
Implement v2.0.0: Production migration from appnew.py to app.py

Breaking Changes:
- Rename app.py → app_v1.py (legacy preserved)
- Rename appnew.py → app.py (now production)
- Update docker-compose.yaml to reference app.py
- Add Streamlit headless mode flags to disable email prompt

Documentation:
- Update CLAUDE.md with app.py references
- Mark v1.0.2-v1.0.10 as Released in project_requirements.md
- Update README.md with v2.0 features

Configuration:
- Update VERSION to 2.0.0 in constants.py
- Configure Streamlit with --server.headless true flag
- Update .vscode/launch.json for new entry point

Deployment:
- Docker Compose entry point now uses app.py
- CI/CD pipeline unchanged (automatic deployment)
- All v1.0.x features included in v2.0.0

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Post-Deployment:**
- [ ] Verify GitHub Actions workflow completed successfully
- [ ] Verify Docker image tagged with `latest` and commit SHA
- [ ] Verify Kubernetes pod is running (if applicable)
- [ ] Perform production smoke test:
  - [ ] Access production URL
  - [ ] Login with test account
  - [ ] Send test message
  - [ ] Verify response
- [ ] Check error logs in production (first 1 hour)
- [ ] Monitor user feedback (first 24 hours)
- [ ] Update `docs/project_requirements.md` with actual release date
- [ ] Update `docs/versions/README.md` with actual release date
- [ ] Announce deployment to IST256 students (Canvas/Blackboard announcement)

### Rollback Procedure (if needed)

If critical issues arise after deployment:

1. **Immediate Rollback:**
   ```bash
   git revert HEAD
   git push origin main
   ```
   This will trigger automatic redeployment of previous version.

2. **Manual Rollback (if git revert fails):**
   ```bash
   git checkout main
   git reset --hard HEAD~1
   git push --force origin main
   ```
   ⚠️ **Use with caution** - force push can cause issues for team members.

3. **File-Level Rollback:**
   ```bash
   mv app/chat/app.py app/chat/appnew.py
   mv app/chat/app_v1.py app/chat/app.py
   git add app/chat/
   git commit -m "HOTFIX: Rollback to v1 due to production issue"
   git push origin main
   ```

4. **Verify Rollback:**
   - [ ] Check production URL
   - [ ] Verify legacy app is running
   - [ ] Test basic functionality
   - [ ] Monitor error logs

5. **Post-Rollback Actions:**
   - [ ] Document issue in GitHub Issues
   - [ ] Create post-mortem document
   - [ ] Create hotfix branch to address issue
   - [ ] Re-test before re-deploying v2.0.0

## Dependencies

### Internal Dependencies

**Required Versions (must be complete):**
- v1.0.2: Authentication & Authorization ✓
- v1.0.3: Database & Logging Infrastructure ✓
- v1.0.4: LLM Integration ✓
- v1.0.5: Context Injection ✓
- v1.0.6: Chat Logging ✓
- v1.0.7: Admin Menu ✓
- v1.0.8: UI Polish ✓
- v1.0.9: Export Logs ✓
- v1.0.10: Persistent User Preferences ✓

### External Dependencies

**Runtime Dependencies (from requirements.txt):**
- streamlit >= 1.30 (for headless mode)
- sqlalchemy
- sqlmodel
- psycopg2-binary
- minio
- msal
- openai (for Azure OpenAI)
- ollama (for Ollama backend)

**Infrastructure Dependencies:**
- PostgreSQL database (accessible via DATABASE_URL)
- MinIO S3 (accessible via S3_HOST)
- Azure OpenAI or Ollama instance (accessible via API keys)
- Azure AD tenant (for MSAL authentication)

### Team Dependencies

- **Instructor approval** for production deployment
- **Code review** from team member or instructor
- **Access credentials** for production deployment (if not automated)

## Risks & Mitigation

### Risk 1: File rename breaks imports

- **Impact**: High (application won't start)
- **Probability**: Low (all imports are relative)
- **Mitigation**:
  - Thoroughly test locally before deployment
  - Use `git mv` to preserve file history
  - Verify imports with `python -m py_compile app/chat/app.py`

### Risk 2: Docker build fails due to missing file

- **Impact**: High (can't deploy)
- **Probability**: Low (file rename is straightforward)
- **Mitigation**:
  - Test Docker build locally before pushing
  - Add `COPY app/chat/app.py /app/app.py` to Dockerfile if needed
  - Verify file paths in Dockerfile

### Risk 3: Streamlit email prompt still appears

- **Impact**: Medium (annoying but not blocking)
- **Probability**: Low (flags are well-documented)
- **Mitigation**:
  - Test with `--server.headless true` flag locally
  - Add `.streamlit/config.toml` as backup configuration
  - Use Streamlit version >= 1.30

### Risk 4: Feature regression (v2.0 missing v1 functionality)

- **Impact**: High (users can't complete tasks)
- **Probability**: Low (all features in v1.0.2-v1.0.10)
- **Mitigation**:
  - Perform comprehensive manual testing (Phase 5)
  - Keep `app_v1.py` for emergency rollback
  - Test all user types (admin, exception, roster)
  - Test all user flows (login, chat, admin, export, preferences)

### Risk 5: Database migration issues

- **Impact**: Low (no schema changes)
- **Probability**: Very Low (v2.0.0 has no DB changes)
- **Mitigation**:
  - No migration needed
  - Forward-compatible schema from v1.0.10

### Risk 6: User confusion from UI changes

- **Impact**: Low (v2.0 UI is already tested in v1.0.x)
- **Probability**: Low (users already using `appnew.py` in development)
- **Mitigation**:
  - Announce deployment to students via Canvas/Blackboard
  - Provide help documentation in app (TIPS_TEXT, FAQ_TEXT)
  - Monitor user feedback in first week

## Success Criteria

**Deployment Success:**
- [ ] VERSION constant is "2.0.0"
- [ ] `app.py` exists and contains v2.0 code
- [ ] `app_v1.py` exists and contains legacy code
- [ ] Docker Compose uses `app.py` as entry point
- [ ] Streamlit email prompt does not appear
- [ ] All Phase 5 tests passing
- [ ] All documentation updated (CLAUDE.md, README.md, project_requirements.md)

**Functional Success:**
- [ ] Users can login via Azure AD
- [ ] Users can select Tutor or Answer mode
- [ ] Users can select assignment context
- [ ] LLM generates responses to user prompts
- [ ] Chat messages are logged to PostgreSQL
- [ ] User preferences persist across sessions
- [ ] Admin users can access Settings, Prompts, Export, Session pages
- [ ] Admin users can export logs as CSV or JSON
- [ ] Non-admin users cannot access admin menu

**Production Success:**
- [ ] Code merged to `main` branch
- [ ] CI/CD pipeline passed
- [ ] Docker image built and pushed to registry
- [ ] Application deployed to production environment
- [ ] Production smoke test passed (login + send message)
- [ ] No critical bugs reported within 24 hours
- [ ] No rollback required within 48 hours

## Post-Deployment

### Monitoring

**Metrics to Watch (first 24 hours):**
- Application uptime (should be 100%)
- Error rate in logs (should be < 1% of requests)
- Authentication success rate (should be > 95%)
- LLM response latency (should be < 10 seconds)
- Database query performance (should be < 100ms per query)

**Log Monitoring:**
- Check Streamlit logs for startup errors
- Check PostgreSQL logs for connection issues
- Check application logs for LLM API errors
- Check Kubernetes pod logs (if applicable)

**User Feedback:**
- Monitor IST256 course channels (Discord, Slack, Canvas discussions)
- Respond to bug reports within 4 hours
- Collect feature requests for future versions

### Follow-up Tasks

- [ ] Update course documentation (syllabus, assignment instructions) if app features mentioned
- [ ] Create user guide video/tutorial for v2.0 features (optional)
- [ ] Schedule retrospective meeting to review v2.0 migration process
- [ ] Document lessons learned in project wiki
- [ ] Plan next version (v2.0.1 or v2.1.0) based on user feedback
- [ ] Archive legacy `app_v1.py` after 30 days of successful v2.0 operation (optional)

### Performance Baseline

**Establish v2.0 Performance Baseline (first week):**
- Average response time for user prompts
- Average database query latency
- Average S3 config load time
- Peak concurrent users
- Memory usage per session
- CPU usage during LLM streaming

**Use this baseline for:**
- Future performance optimization efforts
- Identifying performance regressions in v2.1.0+
- Capacity planning for next semester

---

**Generated**: 2025-12-28
**Author**: AI-assisted planning via /design command
**Version**: 2.0.0
