# Implementation Plan: Settings Simplification - v2.1.0

## Timeline

- **Estimated effort**: 3-5 hours
- **Complexity**: Medium
- **Dependencies**: v2.0.1 must be complete

## Phase 1: Preparation

### Tasks

- [ ] Review technical specification (`docs/versions/v2.1.0/technical-spec.md`)
- [ ] Set up development branch: `feature/v2.1.0-settings-simplification`
- [ ] Verify S3 access and current config.yaml contents
- [ ] Review existing prompts.yaml structure for migration reference

### Prerequisites

- v2.0.1 complete and deployed
- S3 access configured and working
- Admin credentials available for testing

## Phase 2: Backend Implementation - Data Models

### Tasks

- [ ] Rename `ConfigurationModel` to `AppSettingsModel` in models.py
- [ ] Add `answer_prompt` field with default value
- [ ] Add `tutor_prompt` field with default value
- [ ] Remove `system_prompt` field (the selector key)
- [ ] Remove `system_prompt_text` field (no longer needed)
- [ ] Update `from_yaml_string()` to load new fields gracefully with defaults
- [ ] Update `to_yaml_string()` to serialize new fields

### Files to Modify

- `/workspaces/ist256-chatapp/app/dal/models.py`
  - **Changes**: Rename class, add prompt fields, update serialization
  - **Lines**: 26-65 (ConfigurationModel class)
  - **Reason**: Consolidate prompts into main settings model

### Default Values

```python
DEFAULT_AI_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_ANSWER_PROMPT = "Your name is Answerbot. You're have knowledge of Python programming."
DEFAULT_TUTOR_PROMPT = "Your name is Tutorbot. You're a supportive AI Python programming tutor."
DEFAULT_WHITELIST = ""
```

## Phase 3: Backend Implementation - App Updates

### Tasks

- [ ] Update all imports from `ConfigurationModel` to `AppSettingsModel`
- [ ] Remove prompts.yaml loading block
- [ ] Remove `st.session_state.prompts` references
- [ ] Update `set_context()` to use `config.tutor_prompt` and `config.answer_prompt`
- [ ] Update LLM initialization to use config prompt fields directly
- [ ] Remove "Prompts" from admin menu options
- [ ] Remove prompts page import and routing

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/app.py`
  - **Changes**: Update imports, remove prompts.yaml loading, update prompt references
  - **Lines to update**:
    - Line 23: Import statement change
    - Lines 46-54: Update `set_context()` prompt lookup
    - Lines 240-249: Remove prompts_yaml loading and session state
    - Lines 267-269: Update mode-to-prompt mapping
    - Lines 160-161: Remove "Prompts" from admin menu
    - Lines 319-326: Remove Prompts page routing
  - **Reason**: Align app with new AppSettingsModel structure

### Code Changes Detail

**Import change (line 23):**
```python
# Before
from dal.models import AuthModel, ConfigurationModel

# After
from dal.models import AuthModel, AppSettingsModel
```

**set_context() prompt lookup (lines 46-54):**
```python
# Before
mode_to_prompt_name = {"Tutor": "tutor", "Answer": "answer"}
prompt_name = mode_to_prompt_name[mode]
base_system_prompt = st.session_state.prompts[prompt_name]

# After
if mode == "Tutor":
    base_system_prompt = st.session_state.config.tutor_prompt
else:
    base_system_prompt = st.session_state.config.answer_prompt
```

**Config loading (lines 235-250):**
```python
# Before
if 'config' not in st.session_state:
    config_yaml = st.session_state.s3_client.get_text_file(...)
    prompts_yaml = st.session_state.s3_client.get_text_file(...)  # Remove this
    config = ConfigurationModel.from_yaml_string(config_yaml)
    prompts = yaml.safe_load(prompts_yaml)['prompts']  # Remove this
    st.session_state.config = config
    st.session_state.prompts = prompts  # Remove this
    st.session_state.system_prompt_text = prompts[config.system_prompt]  # Remove this

# After
if 'config' not in st.session_state:
    config_yaml = st.session_state.s3_client.get_text_file(...)
    config = AppSettingsModel.from_yaml_string(config_yaml)
    st.session_state.config = config
```

**Admin menu (lines 159-165):**
```python
# Before
options=["Chat", "Settings", "Prompts", "Export", "Session"]

# After
options=["Chat", "Settings", "Export", "Session"]
```

## Phase 4: Frontend Implementation - Settings Page

### Tasks

- [ ] Remove prompts.yaml loading code
- [ ] Update to use `AppSettingsModel` instead of `ConfigurationModel`
- [ ] Add "System Prompts" section header
- [ ] Add `st.text_area` for Tutor Mode Prompt
- [ ] Add `st.text_area` for Answer Mode Prompt
- [ ] Remove system_prompt selectbox
- [ ] Remove prompt preview section (no longer needed)
- [ ] Update save logic to include prompt fields

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/settings.py`
  - **Changes**: Complete rewrite of settings page
  - **Lines**: 1-63 (entire file)
  - **Reason**: Simplify to single config model with inline prompts

### New Settings Page Structure

```python
def show_settings():
    s3client = S3Client(...)

    config_yaml = s3client.get_text_file(
        os.environ["S3_BUCKET"],
        os.environ["CONFIG_FILE"],
        fallback_file_path=os.environ.get("CONFIG_FILE_FALLBACK", "/app/data/config.yaml")
    )
    config = AppSettingsModel.from_yaml_string(config_yaml)
    bucket_files = s3client.list_objects(os.environ["S3_BUCKET"], prefix="")
    whitelist_files = [f for f in bucket_files if not f.endswith('.yaml')]

    st.title("Settings")
    st.markdown("Configure AI model settings and system prompts.")

    # Model Settings Section
    st.header("Model Settings")
    ai_model = st.text_input("AI Model", value=config.ai_model)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0,
                           value=float(config.temperature), step=0.05)
    whitelist = st.selectbox("Whitelist File", options=whitelist_files,
                            index=whitelist_files.index(config.whitelist)
                            if config.whitelist in whitelist_files else 0)

    # System Prompts Section
    st.header("System Prompts")
    st.markdown("Configure the AI's behavior in each mode.")

    tutor_prompt = st.text_area(
        "Tutor Mode Prompt",
        value=config.tutor_prompt,
        height=200,
        help="Used when AI mode is 'Tutor' - guides students with questions"
    )

    answer_prompt = st.text_area(
        "Answer Mode Prompt",
        value=config.answer_prompt,
        height=200,
        help="Used when AI mode is 'Answer' - provides direct answers"
    )

    # Save Button
    submitted = st.button("Save Settings")
    if submitted:
        config.ai_model = ai_model
        config.temperature = temperature
        config.whitelist = whitelist
        config.tutor_prompt = tutor_prompt
        config.answer_prompt = answer_prompt

        yaml_string = config.to_yaml_string()
        s3client.put_text_file(os.environ["S3_BUCKET"], os.environ["CONFIG_FILE"], yaml_string)
        st.success("Settings saved successfully!")
        if st.button("Restart Application"):
            st.session_state.clear()
            st.rerun()
```

## Phase 5: Cleanup - Delete Prompts Page

### Tasks

- [ ] Delete `/workspaces/ist256-chatapp/app/chat/prompts.py`
- [ ] Verify no remaining imports of `prompts.py`
- [ ] Optionally update default config.yaml template in `/app/data/`

### Files to Delete

- `/workspaces/ist256-chatapp/app/chat/prompts.py`
  - **Reason**: Functionality moved to settings.py

### Optional File Updates

- `/workspaces/ist256-chatapp/app/data/config.yaml`
  - **Changes**: Update default template to include prompt fields
  - **Reason**: Provide correct defaults for new installations

## Phase 6: Configuration & Constants

### Tasks

- [ ] Update `VERSION = "2.1.0"` in constants.py
- [ ] Optionally update `/app/data/config.yaml` template

### Files to Modify

- `/workspaces/ist256-chatapp/app/chat/constants.py`
  - **Changes**: Update VERSION constant on line 1
  - **Before**: `VERSION="2.0.1f"`
  - **After**: `VERSION="2.1.0"`

## Phase 7: Testing

### Manual Testing Checklist

#### Settings Page
- [ ] Admin can access Settings page
- [ ] Settings page displays "Model Settings" section
- [ ] AI Model text input shows current value
- [ ] Temperature slider shows current value (0.0 to 1.0)
- [ ] Whitelist dropdown shows available files
- [ ] Settings page displays "System Prompts" section
- [ ] Tutor Mode Prompt text area shows current prompt
- [ ] Answer Mode Prompt text area shows current prompt
- [ ] "Save Settings" button is visible
- [ ] Saving settings shows success message
- [ ] Saved values persist after page refresh

#### Admin Menu
- [ ] Admin menu shows: Chat, Settings, Export, Session
- [ ] "Prompts" option is NOT in admin menu
- [ ] Clicking Settings navigates to settings page
- [ ] Other admin pages still work

#### Chat Functionality
- [ ] Tutor mode uses tutor_prompt from config
- [ ] Answer mode uses answer_prompt from config
- [ ] Context injection still works with new prompts
- [ ] Mode switching still clears history and updates prompt

#### Edge Cases
- [ ] App loads without config.yaml (uses defaults)
- [ ] App loads with old config.yaml format (missing prompts, uses defaults)
- [ ] Empty prompt fields save correctly
- [ ] Very long prompts save and load correctly
- [ ] Non-admin users cannot access Settings page

### Integration Testing

- [ ] S3 config.yaml updated with new fields after save
- [ ] ChatLogger still logs correctly
- [ ] LLM responses use correct prompt for mode
- [ ] User preferences still load/save correctly

## Phase 8: Documentation

### Tasks

- [ ] Update CLAUDE.md if configuration section mentions prompts.yaml
- [ ] Update docs/versions/README.md with v2.1.0 entry
- [ ] Update project_requirements.md status to Released

### Files to Update

- `/workspaces/ist256-chatapp/CLAUDE.md`
  - **Section**: Configuration Files
  - **Changes**: Update to show new config.yaml structure without prompts.yaml
  - **Lines**: ~190-210 (Configuration Files section)

- `/workspaces/ist256-chatapp/docs/versions/README.md`
  - **Changes**: Add v2.1.0 row to version table

## Phase 9: Deployment

### Tasks

- [ ] Commit changes: "Implement v2.1.0: Settings simplification - consolidate prompts into config"
- [ ] Push feature branch to remote
- [ ] Create PR to main branch
- [ ] Code review
- [ ] Merge to main
- [ ] Verify CI/CD pipeline passes
- [ ] Monitor deployment logs
- [ ] Verify settings page works in production

### Deployment Checklist

- [ ] All manual tests passing locally
- [ ] No merge conflicts with main
- [ ] VERSION constant updated to 2.1.0
- [ ] prompts.py deleted
- [ ] Admin menu updated (no Prompts option)
- [ ] Settings page shows prompt text areas

### Post-Deployment

- [ ] Verify admin can access Settings page in production
- [ ] Verify prompts can be edited and saved
- [ ] Verify chat modes use correct prompts
- [ ] Monitor logs for errors

## Dependencies

### Internal Dependencies

- v2.0.1 (S3 fallback handling) must be complete
- S3 bucket must be accessible

### External Dependencies

- None new - uses existing streamlit, pydantic, yaml

## Risks & Mitigation

### Risk 1: Existing config.yaml missing new fields

- **Impact**: Low
- **Probability**: High (expected during migration)
- **Mitigation**: `from_yaml_string()` provides defaults for missing fields

### Risk 2: Admin saves settings, breaks prompts

- **Impact**: Medium
- **Probability**: Low
- **Mitigation**: UI validates that prompts are non-empty; defaults always available

### Risk 3: Users notice prompt changes

- **Impact**: Low
- **Probability**: Low
- **Mitigation**: Initial prompts use same content as current prompts.yaml

## Success Criteria

- [ ] prompts.py file deleted
- [ ] Admin menu has 4 options (Chat, Settings, Export, Session)
- [ ] Settings page shows prompt text areas
- [ ] Prompts save to config.yaml in S3
- [ ] Chat modes use correct prompts
- [ ] App loads gracefully with missing prompt fields
- [ ] No errors in production logs
- [ ] VERSION displays 2.1.0 in UI

## Rollback Procedure

1. Revert merge commit on main branch
2. Re-deploy previous version
3. Restore prompts.yaml to S3 if deleted
4. Verify prompts.py is accessible
5. Verify admin menu shows "Prompts" option
6. Test settings and prompts pages work

---

**Generated**: 2026-01-13
**Author**: AI-assisted planning via /design command
**Version**: 2.1.0
**Status**: As of 2026-01-13, implementation is mostly complete (backend and frontend done). Needs: admin menu cleanup, documentation updates, and testing verification.
