# Implementation Plan: Context Injection Enhancement - v1.0.5

## Timeline

- Estimated effort: 4-5 hours
- Complexity: Medium
- Suggested sprint: Single development session

## Phase 1: Preparation

### Tasks

- [ ] Review technical specification: [/workspaces/ist256-chatapp/docs/versions/v1.0.5/technical-spec.md](/workspaces/ist256-chatapp/docs/versions/v1.0.5/technical-spec.md)
- [ ] Set up development branch: `feature/v1.0.5-context-injection`
- [ ] Verify v1.0.4 (LLM integration) is complete and tested
- [ ] Verify v1.0.2 (authentication) is complete and AuthModel.firstname available
- [ ] Test FileCacheDocLoader.load_cached_document() works correctly
- [ ] Verify assignment .md files exist in LOCAL_FILE_CACHE directory

### Prerequisites

**Required Completed Versions:**
- v1.0.2 (Authentication & Authorization) - MUST be complete
- v1.0.4 (LLM Integration) - MUST be complete

**Environment Requirements:**
- `LOCAL_FILE_CACHE` env var set and directory populated with assignment markdown files
- At least one test assignment file (e.g., `Intro-01-Lab.md`) for testing

**Verification Commands:**
```bash
# Check assignment files exist
ls -lh $LOCAL_FILE_CACHE

# Verify v1.0.4 is current version
grep VERSION /workspaces/ist256-chatapp/app/chat/constants.py

# Test authentication in appnew.py
streamlit run /workspaces/ist256-chatapp/app/chat/appnew.py
# → Login and verify st.session_state.auth_model.firstname is populated
```

## Phase 2: Backend Implementation

### Tasks

- [ ] Update `get_context_injection()` function signature to accept `system_prompt` parameter
- [ ] Modify `get_context_injection()` to prepend assignment content to system prompt
- [ ] Add error handling for FileNotFoundError in `get_context_injection()`
- [ ] Update `set_context()` to apply context injection to AI system prompt
- [ ] Add personalized greeting with user's firstname
- [ ] Add defensive check for missing firstname in AuthModel
- [ ] Test context injection with both Tutor and Answer modes
- [ ] Test context switch clears old context and applies new one

### Files to Modify

#### [/workspaces/ist256-chatapp/app/chat/appnew.py](/workspaces/ist256-chatapp/app/chat/appnew.py)

**Change 1: Update `get_context_injection()` function (lines 52-58)**

**Old Code:**
```python
def get_context_injection(context: str) -> str:
    """Returns the context injection prompt based on the selected context."""
    if context != "General Python":
        content = st.session_state.file_cache.load_cached_document(context)
        return const.CONTEXT_PROMPT_TEMPLATE.format(assignment=context, content=content)
    else:
        return ""
```

**New Code:**
```python
def get_context_injection(context: str, system_prompt: str) -> str:
    """
    Returns enhanced system prompt with context injection if applicable.

    Args:
        context: The assignment context or "General Python"
        system_prompt: The base system prompt (from prompts.yaml based on mode)

    Returns:
        Complete system prompt with context prepended if applicable
    """
    if context != "General Python":
        try:
            content = st.session_state.file_cache.load_cached_document(context)
            context_injection = const.CONTEXT_PROMPT_TEMPLATE.format(
                assignment=context,
                content=content
            )
            logger.info(f"Context injected: {context}, size: {len(content)} chars")
            return context_injection + "\n\n" + system_prompt
        except FileNotFoundError:
            logger.error(f"Assignment file not found: {context}")
            st.warning(f"Assignment content for '{context}' is not available. Using general mode.")
            return system_prompt
        except Exception as e:
            logger.error(f"Error loading assignment {context}: {e}")
            st.warning(f"Unable to load assignment context. Please try again or select 'General Python'.")
            return system_prompt
    else:
        return system_prompt
```

**Reason**: Prepend assignment content to system prompt instead of returning separate injection string. Add error handling for missing files.

---

**Change 2: Update `set_context()` to apply context injection (lines 26-44)**

**Add after line 33** (after `st.session_state.context = context`):
```python
# Apply context injection to AI system prompt if AI is initialized
if 'ai' in st.session_state and 'prompts' in st.session_state:
    mode_to_prompt_name = {"Tutor": "learning", "Answer": "original"}
    prompt_name = mode_to_prompt_name[mode]
    base_system_prompt = st.session_state.prompts[prompt_name]

    # Get context-enhanced system prompt
    enhanced_system_prompt = get_context_injection(context, base_system_prompt)
    st.session_state.ai.system_prompt = enhanced_system_prompt
    logger.info(f"System prompt updated: mode={mode}, context={context}")
```

**Reason**: Apply context injection when context is set, ensuring LLM has full assignment context before conversation starts.

**Note**: Remove the existing system prompt update code that's currently in lines 40-44 since it will be redundant.

---

**Change 3: Update greeting with user's firstname (lines 232-242)**

**Old Code:**
```python
#setup the initial AI context_message based on mode and context
if st.session_state.new_session_context:

    with st.chat_message("assistant", avatar=avatars["assistant"]):
        with st.spinner("Thinking..."):
            if st.session_state.mode == "Tutor":
                greeting = f"I am in Tutor mode. I  will provide guided learning for your {st.session_state.context} questions\n"
            else:
                greeting = f"I am in Answer mode. I will provide direct answers to your {st.session_state.context} questions\n"
            st.write_stream(stream_text(greeting))

    st.session_state.new_session_context = False
```

**New Code:**
```python
#setup the initial AI context_message based on mode and context
if st.session_state.new_session_context:

    with st.chat_message("assistant", avatar=avatars["assistant"]):
        with st.spinner("Thinking..."):
            # Get user's firstname with fallback
            firstname = st.session_state.auth_model.firstname if hasattr(st.session_state.auth_model, 'firstname') and st.session_state.auth_model.firstname else "Student"

            if st.session_state.mode == "Tutor":
                greeting = f"Hello {firstname}! I am in Tutor mode. I will provide guided learning for your {st.session_state.context} questions.\n"
            else:
                greeting = f"Hello {firstname}! I am in Answer mode. I will provide direct answers to your {st.session_state.context} questions.\n"
            st.write_stream(stream_text(greeting))

    st.session_state.new_session_context = False
```

**Reason**: Personalize greeting with user's firstname from AuthModel. Add defensive check in case firstname is missing.

---

**Change 4: Remove unused context_injection storage (line 34)**

**Delete this line:**
```python
st.session_state.context_injection = get_context_injection(context)
```

**Reason**: No longer storing context_injection separately; it's applied directly to system prompt.

---

#### [/workspaces/ist256-chatapp/app/chat/constants.py](/workspaces/ist256-chatapp/app/chat/constants.py)

**Change 1: Update VERSION constant (line 1)**

**Old Code:**
```python
VERSION="1.0.4"
```

**New Code:**
```python
VERSION="1.0.5"
```

**Reason**: Reflect new version number.

---

**Change 2 (Optional): Refine CONTEXT_PROMPT_TEMPLATE (lines 40-47)**

**Current Code:**
```python
CONTEXT_PROMPT_TEMPLATE='''
I would like to ask you questions about the assignment: {assignment}.
Please acknowledge that you are ready to answer questions about this assignment.

Here is the content of that assignment:

{content}
'''
```

**Recommended Code:**
```python
CONTEXT_PROMPT_TEMPLATE='''
You are assisting with the assignment: {assignment}

Here is the full assignment content:

{content}

---

'''
```

**Reason**: When prepended to system prompt, we don't need the "acknowledge" request since this is context, not a user message. The separator "---" cleanly divides assignment content from base system prompt.

**Decision**: Optional - test with existing template first, refine if needed.

### Files to Create

None.

## Phase 3: Frontend Implementation

### Tasks

No frontend changes required. All changes are backend logic that affect LLM behavior and greeting display.

## Phase 4: Configuration & Constants

### Tasks

- [x] Update `app/chat/constants.py` with VERSION = "1.0.5" (covered in Phase 2)
- [ ] No config.yaml changes needed
- [ ] No prompts.yaml changes needed
- [ ] No environment variable documentation changes needed

### Configuration Changes

None required.

## Phase 5: Testing

### Tasks

- [ ] Manual testing checklist
  - [ ] **Test 1: Context Injection with Assignment**
    - Login as test user
    - Verify greeting includes firstname
    - Select assignment (e.g., "Intro-01-Lab")
    - Verify greeting mentions assignment context
    - Ask question about assignment content
    - Verify LLM response shows knowledge of assignment
  - [ ] **Test 2: General Python Mode**
    - Select "General Python"
    - Verify greeting includes firstname but no assignment
    - Ask general Python question
    - Verify LLM provides standard response
  - [ ] **Test 3: Context Switching**
    - Select "Intro-01-Lab"
    - Ask "What variables are used?"
    - Note response
    - Switch to "Intro-02-Lab"
    - Ask "What variables are used?"
    - Verify response references Intro-02, not Intro-01
  - [ ] **Test 4: Mode Switching**
    - Start in Tutor mode with context
    - Ask question, observe Socratic response
    - Switch to Answer mode
    - Ask question, observe direct answer
    - Verify context persists across mode change
  - [ ] **Test 5: Admin User**
    - Login as admin user
    - Verify context injection works same as roster user
  - [ ] **Test 6: Roster User**
    - Login as roster user
    - Verify full context injection functionality
  - [ ] **Test 7: Error Handling - Missing File**
    - Temporarily rename one .md file in file cache
    - Select that assignment
    - Verify warning displayed
    - Verify fallback to general mode (no crash)
    - Restore file
  - [ ] **Test 8: Both LLM Backends**
    - Test with LLM=azure (default)
    - Test with LLM=ollama (if available)
    - Verify context injection works with both

- [ ] Integration testing
  - [ ] Database integration: Verify no errors (logging not yet implemented in v1.0.5)
  - [ ] S3 integration: Verify prompts.yaml loads correctly
  - [ ] FileCacheDocLoader integration: Verify assignments load correctly
  - [ ] LLMAPI integration: Verify system_prompt updates correctly

- [ ] Performance testing
  - [ ] Load large assignment (if any >50KB)
  - [ ] Verify response time acceptable
  - [ ] Check LLM token usage in logs

### Test Data

**Required:**
- At least 2 different assignment markdown files in LOCAL_FILE_CACHE
- Test user accounts: 1 admin, 1 roster, 1 exception
- Both Azure OpenAI and Ollama endpoints configured (optional for Ollama)

**Test Assignments:**
- Intro-01-Lab.md (small assignment)
- Intro-02-Lab.md (for context switching test)

**Expected Greeting Examples:**
- Tutor mode + General Python: "Hello Mike! I am in Tutor mode. I will provide guided learning for your General Python questions."
- Answer mode + Intro-01-Lab: "Hello Mike! I am in Answer mode. I will provide direct answers to your Intro-01-Lab questions."

## Phase 6: Documentation

### Tasks

- [ ] Update README.md (if user-facing changes)
  - No changes needed - context injection is transparent to users
- [ ] Update CLAUDE.md with context injection details
  - Add explanation of context injection in "Chat Flow" section
  - Update "System Prompts" section to explain context prepending
- [ ] Add inline code comments for complex logic
  - Comment explaining context injection strategy in get_context_injection()
  - Comment explaining firstname fallback logic
- [ ] Update docs/versions/README.md with v1.0.5 entry
  - Mark as "In Development" initially
  - Update to "Released" after deployment

### Documentation Files

- [/workspaces/ist256-chatapp/CLAUDE.md](/workspaces/ist256-chatapp/CLAUDE.md)
  - Update "Chat Flow" section (lines ~30-40) to explain context injection
  - Update "RAG Implementation" section (lines ~60-70) to reflect always-on context
- [/workspaces/ist256-chatapp/docs/versions/README.md](/workspaces/ist256-chatapp/docs/versions/README.md)
  - Add v1.0.5 row to version history table
- [/workspaces/ist256-chatapp/README.md](/workspaces/ist256-chatapp/README.md)
  - No changes needed

## Phase 7: Deployment

### Tasks

- [ ] Commit changes with message: "Implement v1.0.5: Context Injection Enhancement"
- [ ] Push feature branch to remote
- [ ] Create PR to main branch
- [ ] Code review (if team review process exists)
- [ ] Address review feedback
- [ ] Merge to main
- [ ] Verify CI/CD pipeline passes
- [ ] Monitor deployment
- [ ] Verify in production environment

### Deployment Checklist

- [ ] All tests passing
- [ ] No merge conflicts
- [ ] VERSION = "1.0.5" in constants.py
- [ ] Documentation complete (CLAUDE.md, version docs)
- [ ] No breaking changes
- [ ] Feature tested with both Azure and Ollama (if both in use)

### Commit Message Template

```
Implement v1.0.5: Context Injection Enhancement

- Always-on context injection when assignment selected
- Prepend assignment content to system prompt
- Personalized greeting with user's firstname
- Enhanced error handling for missing assignment files
- Remove experimental RAG assignment logic

Closes: #[issue-number] (if applicable)
Depends on: v1.0.4 (LLM Integration), v1.0.2 (Authentication)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Dependencies

### Internal Dependencies

**Required Completed Versions:**
- v1.0.2 (Authentication & Authorization)
  - Provides: `AuthModel.firstname` for personalized greeting
  - Provides: User authentication and session state
- v1.0.4 (LLM Integration)
  - Provides: `LLMAPI` with `system_prompt` attribute
  - Provides: Mode-based system prompt selection
  - Provides: Streaming LLM responses

**Required Components:**
- FileCacheDocLoader (already exists in app/chat/docloader.py)
- Assignment markdown files in LOCAL_FILE_CACHE directory
- S3 client for loading prompts.yaml (already in v1.0.3)

### External Dependencies

None. All dependencies already in requirements.txt:
- streamlit
- loguru (for logging)
- PyYAML (for config loading)

### Team Dependencies

None. Single developer implementation.

## Risks & Mitigation

### Risk 1: Assignment File Missing or Corrupted

- **Impact**: Medium (feature fails for specific assignment, not entire app)
- **Probability**: Low (files are pre-loaded by ETL pipeline)
- **Mitigation**:
  - Add try/except error handling in `get_context_injection()`
  - Display user-friendly warning message
  - Fallback to base system prompt (no crash)
  - Log error for admin investigation
  - **Action**: Implemented in Phase 2

### Risk 2: Large Assignment Exceeds LLM Context Window

- **Impact**: Low (LLM will truncate or fail gracefully)
- **Probability**: Very Low (assignments are 5-20KB, well within 128K token limit)
- **Mitigation**:
  - Current assignments tested and within limits
  - Monitor logs for context length warnings
  - If issue arises in future, implement content truncation
  - **Action**: Monitor during testing

### Risk 3: MSAL Token Missing Firstname Claim

- **Impact**: Low (greeting uses "Student" instead of name)
- **Probability**: Very Low (Syracuse AD always provides name)
- **Mitigation**:
  - Defensive check: `if hasattr(st.session_state.auth_model, 'firstname') and st.session_state.auth_model.firstname`
  - Fallback to "Student" if missing
  - **Action**: Implemented in Phase 2

### Risk 4: Mode Switch Doesn't Update System Prompt

- **Impact**: Medium (wrong prompt style used)
- **Probability**: Low (logic tested in v1.0.4)
- **Mitigation**:
  - Comprehensive testing in Phase 5
  - Verify mode_to_prompt_name mapping works with context injection
  - **Action**: Test scenario #4 in testing phase

### Risk 5: Breaking Change from v1.0.4

- **Impact**: High (users unable to chat)
- **Probability**: Very Low (additive feature, no breaking changes)
- **Mitigation**:
  - Code review before merge
  - Test both upgraded users and new users
  - Rollback plan ready (revert commit)
  - **Action**: Follow deployment checklist

## Success Criteria

- [ ] All Phase 5 tests passing
- [ ] VERSION = "1.0.5" in constants.py
- [ ] All documentation updated
- [ ] Code reviewed and approved (if process exists)
- [ ] Deployed to production
- [ ] No critical bugs reported within 24 hours
- [ ] Feature functions as specified in requirements:
  - [ ] Context always injected when assignment selected
  - [ ] Greeting includes user's firstname
  - [ ] LLM responses show assignment awareness
  - [ ] Context switching works correctly
  - [ ] Mode switching works correctly
  - [ ] Error handling graceful for missing files

**Quantitative Criteria:**
- [ ] Context injection working for >95% of assignment selections
- [ ] No increase in error rate from v1.0.4 baseline
- [ ] Response time <5 seconds for typical queries (same as v1.0.4)

## Rollback Procedure

### If Critical Issue Arises

1. **Identify Issue**
   - User reports missing context awareness
   - Errors loading assignment files
   - Firstname not displaying in greeting

2. **Execute Rollback**
   ```bash
   # Revert commit
   git revert <commit-hash-of-v1.0.5>

   # Update VERSION constant
   # Edit app/chat/constants.py: VERSION = "1.0.4"

   # Push rollback
   git push origin main
   ```

3. **Verify Rollback**
   - Check CI/CD pipeline completes
   - Verify version in UI footer shows "v1.0.4"
   - Test basic chat functionality works
   - Verify greeting does not include firstname

4. **Communicate**
   - Notify users of temporary rollback (if applicable)
   - Log issue in GitHub Issues
   - Plan fix and re-deployment

5. **Post-Rollback Actions**
   - Investigate root cause
   - Fix issue in feature branch
   - Retest thoroughly
   - Re-deploy when ready

### Rollback Impact

- **Database**: No schema changes, no rollback needed
- **Configuration**: No config changes, no rollback needed
- **User Experience**: Loss of personalized greetings and context injection, but core functionality intact

## Post-Deployment

### Monitoring

**Key Metrics to Watch (first 24-48 hours):**

1. **Error Rates**
   - Monitor application logs for FileNotFoundError
   - Check for warnings about missing assignment files
   - Alert if error rate >1% of context selections

2. **Performance**
   - Monitor LLM response times (should be similar to v1.0.4)
   - Check for increased token usage in Azure OpenAI dashboard
   - Alert if response time >10 seconds consistently

3. **User Behavior**
   - Track context selection usage (if analytics available)
   - Monitor if users avoid certain assignments (could indicate file issues)

4. **System Health**
   - Streamlit app uptime
   - Database connection health
   - S3 connection health

**Monitoring Tools:**
- Application logs via loguru
- Azure OpenAI usage dashboard
- Kubernetes pod logs (if deployed in K8s)

**Alert Conditions:**
- Error rate >1% on context selection
- Response time >10 seconds for >5% of requests
- App crashes or restarts

### Follow-up Tasks

- [ ] Verify all 24 assignment files load correctly in production
- [ ] Check Azure OpenAI token usage increase (expected: ~30-50%)
- [ ] Gather user feedback on personalized greetings (optional)
- [ ] Document any edge cases discovered during production use
- [ ] Prepare for v1.0.6 (Chat Logging) implementation

**Optional Enhancements for Future Versions:**
- Add assignment summary to greeting (e.g., "This lab covers variables and strings")
- Implement assignment search/filtering if list grows beyond 24
- Add "Recently Used" assignments list
- Analytics on most frequently selected assignments

---

**Generated**: 2025-12-27
**Author**: AI-assisted planning via /design command
**Version**: 1.0.5
