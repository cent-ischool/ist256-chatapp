# Technical Specification: Settings Simplification - v2.1.0

## Overview

This version simplifies the settings architecture by consolidating prompts into the main configuration model. The separate prompts.yaml file and prompts.py admin page are eliminated, and the two mode-specific system prompts (Tutor and Answer) are stored directly in the `AppSettingsModel` (renamed from `ConfigurationModel`). This reduces complexity while maintaining full functionality.

### Features Summary
- Delete prompts.py admin page and all references
- Rename `ConfigurationModel` to `AppSettingsModel`
- Add `answer_prompt` and `tutor_prompt` fields to AppSettingsModel
- Remove `system_prompt` field (no longer needed as a selector)
- Update settings.py to display and edit prompts inline
- Graceful YAML loading with defaults for missing fields

## Architecture Changes

### Components Affected

| File | Change Type | Description |
|------|-------------|-------------|
| `/workspaces/ist256-chatapp/app/dal/models.py` | Modify | Rename ConfigurationModel to AppSettingsModel, add prompt fields |
| `/workspaces/ist256-chatapp/app/chat/settings.py` | Modify | Add inline prompt editing, remove prompts.yaml dependency |
| `/workspaces/ist256-chatapp/app/chat/app.py` | Modify | Update imports and references from ConfigurationModel to AppSettingsModel |
| `/workspaces/ist256-chatapp/app/chat/constants.py` | Modify | Update VERSION to 2.1.0 |

### Components to Delete

| File | Reason |
|------|--------|
| `/workspaces/ist256-chatapp/app/chat/prompts.py` | No longer needed; prompts managed in settings.py |

### Dependencies

- No new external dependencies required
- Existing dependencies: `pydantic`, `yaml`, `streamlit`

## Data Models

### Database Changes

- **No database schema changes** - AppSettingsModel is stored in S3 as YAML, not in PostgreSQL
- Existing `UserPreferencesModel` and `LogModel` remain unchanged

### Model Changes

**Before (ConfigurationModel):**
```python
class ConfigurationModel(BaseModel):
    ai_model: str
    system_prompt: str  # Key to lookup in prompts.yaml ("original" or "learning")
    temperature: float
    whitelist: str
    system_prompt_text: Optional[str] = None
```

**After (AppSettingsModel):**
```python
class AppSettingsModel(BaseModel):
    ai_model: str = "gpt-4o-mini"
    temperature: float = 0.0
    answer_prompt: str = "Your name is Answerbot. You're have knowledge of Python programming."
    tutor_prompt: str = "Your name is Tutorbot. You're a supportive AI Python programming tutor."
    whitelist: str = ""
```

### YAML Structure Changes

**Before (config.yaml + prompts.yaml):**
```yaml
# config.yaml
configuration:
  ai_model: gpt-4o-mini
  system_prompt: learning
  temperature: 0.0
  whitelist: roster.txt

# prompts.yaml
prompts:
  original: "Direct answer mode prompt..."
  learning: "Socratic teaching mode prompt..."
```

**After (config.yaml only):**
```yaml
configuration:
  ai_model: gpt-4o-mini
  temperature: 0.0
  answer_prompt: "Your name is Answerbot. You're have knowledge of Python programming."
  tutor_prompt: "Your name is Tutorbot. You're a supportive AI Python programming tutor."
  whitelist: ""
```

## Technical Design

### Backend Implementation

#### 1. Model Refactoring (`app/dal/models.py`)

```python
class AppSettingsModel(BaseModel):
    ai_model: str = "gpt-4o-mini"
    temperature: float = 0.0
    answer_prompt: str = "Your name is Answerbot. You're have knowledge of Python programming."
    tutor_prompt: str = "Your name is Tutorbot. You're a supportive AI Python programming tutor."
    whitelist: str = ""

    @staticmethod
    def from_yaml_string(yaml_string: str) -> "AppSettingsModel":
        """Load settings gracefully, using defaults for missing fields."""
        try:
            data = yaml.safe_load(yaml_string) or {}
            config = data.get('configuration', {})
            return AppSettingsModel(
                ai_model=config.get('ai_model', 'gpt-4o-mini'),
                temperature=config.get('temperature', 0.0),
                answer_prompt=config.get('answer_prompt', "Your name is Answerbot. You're have knowledge of Python programming."),
                tutor_prompt=config.get('tutor_prompt', "Your name is Tutorbot. You're a supportive AI Python programming tutor."),
                whitelist=config.get('whitelist', '')
            )
        except Exception as e:
            logger.error(f"Error loading AppSettingsModel from YAML: {e}")
            return AppSettingsModel()  # Return defaults

    def to_yaml_string(self) -> str:
        data = {
            'configuration': {
                'ai_model': self.ai_model,
                'temperature': self.temperature,
                'answer_prompt': self.answer_prompt,
                'tutor_prompt': self.tutor_prompt,
                'whitelist': self.whitelist
            }
        }
        return yaml.dump(data)
```

#### 2. Settings Page Update (`app/chat/settings.py`)

Key changes:
- Remove prompts.yaml loading
- Add two `st.text_area` components for tutor_prompt and answer_prompt
- Remove system_prompt selectbox (no longer needed)
- Save prompts directly to config.yaml via AppSettingsModel

#### 3. App.py Updates

- Change all `ConfigurationModel` imports and references to `AppSettingsModel`
- Update prompt lookup from `st.session_state.prompts[prompt_name]` to direct model access:
  - `st.session_state.config.tutor_prompt` (for Tutor mode)
  - `st.session_state.config.answer_prompt` (for Answer mode)
- Remove `st.session_state.prompts` (no longer needed)
- Remove prompts.yaml loading block

### Frontend Implementation

#### Settings Page UI (`settings.py`)

```python
def show_settings():
    # Load config from S3
    config = AppSettingsModel.from_yaml_string(config_yaml)

    st.title("Settings")

    # General settings
    ai_model = st.text_input("AI Model", value=config.ai_model)
    temperature = st.slider("Temperature", 0.0, 1.0, config.temperature, 0.05)
    whitelist = st.selectbox("Whitelist File", options=whitelist_files, ...)

    # Prompt settings (new)
    st.header("System Prompts")
    st.markdown("Configure the system prompts for each AI mode.")

    tutor_prompt = st.text_area(
        "Tutor Mode Prompt",
        value=config.tutor_prompt,
        height=200,
        help="Prompt used when AI is in Tutor mode (Socratic teaching)"
    )

    answer_prompt = st.text_area(
        "Answer Mode Prompt",
        value=config.answer_prompt,
        height=200,
        help="Prompt used when AI is in Answer mode (direct answers)"
    )

    # Save button
    if st.button("Save Settings"):
        config.ai_model = ai_model
        config.temperature = temperature
        config.whitelist = whitelist
        config.tutor_prompt = tutor_prompt
        config.answer_prompt = answer_prompt
        s3client.put_text_file(bucket, config_file, config.to_yaml_string())
        st.success("Settings saved!")
```

### Integration Points

| Component | Integration |
|-----------|-------------|
| **MinIO S3** | Config stored in config.yaml only (prompts.yaml no longer needed) |
| **PostgreSQL** | No changes - logging continues unchanged |
| **LLM API** | Prompts now come from AppSettingsModel fields |
| **Authentication** | No changes - admin check still required for settings |
| **Session State** | Remove `st.session_state.prompts`, use `st.session_state.config` directly |

## Configuration

### Environment Variables

**No changes required.** Existing variables continue to work:
- `CONFIG_FILE` - Points to config.yaml (now contains prompts)
- `CONFIG_FILE_FALLBACK` - Fallback path for config.yaml

**Can be removed (optional cleanup):**
- `PROMPTS_FILE` - No longer needed
- `PROMPTS_FILE_FALLBACK` - No longer needed

### Config Files

**app/data/config.yaml (updated default template):**
```yaml
configuration:
  ai_model: gpt-4o-mini
  temperature: 0.0
  answer_prompt: "Your name is Answerbot. You're have knowledge of Python programming."
  tutor_prompt: "Your name is Tutorbot. You're a supportive AI Python programming tutor."
  whitelist: ""
```

**app/data/prompts.yaml:**
- Can be deleted or kept for reference
- No longer loaded by the application

## Security Considerations

| Consideration | Handling |
|---------------|----------|
| **Admin-only access** | Settings page remains admin-only (unchanged) |
| **Input validation** | Prompts are text fields; no special validation needed |
| **XSS prevention** | Streamlit handles escaping; prompts used only server-side |
| **SQL injection** | N/A - settings stored in S3, not database |

## Performance Considerations

| Aspect | Impact |
|--------|--------|
| **S3 calls** | Reduced by 1 per session (no prompts.yaml load) |
| **Memory** | Slightly reduced (no separate prompts dict) |
| **Startup time** | Slightly faster (one less S3 file to load) |

## Error Handling

### Graceful Defaults

The `from_yaml_string()` method handles missing fields gracefully:

```python
@staticmethod
def from_yaml_string(yaml_string: str) -> "AppSettingsModel":
    try:
        data = yaml.safe_load(yaml_string) or {}
        config = data.get('configuration', {})
        return AppSettingsModel(
            ai_model=config.get('ai_model', 'gpt-4o-mini'),
            temperature=config.get('temperature', 0.0),
            answer_prompt=config.get('answer_prompt', DEFAULT_ANSWER_PROMPT),
            tutor_prompt=config.get('tutor_prompt', DEFAULT_TUTOR_PROMPT),
            whitelist=config.get('whitelist', '')
        )
    except Exception as e:
        logger.error(f"Error loading AppSettingsModel from YAML: {e}")
        return AppSettingsModel()  # Return model with all defaults
```

### Migration Path

When loading existing config.yaml without prompt fields:
1. `from_yaml_string()` returns defaults for missing `answer_prompt` and `tutor_prompt`
2. Admin saves settings -> new fields written to S3
3. Subsequent loads include all fields

## Testing Strategy

### Unit Tests

| Test Case | Description |
|-----------|-------------|
| `test_app_settings_from_yaml_complete` | Load YAML with all fields |
| `test_app_settings_from_yaml_missing_prompts` | Load YAML missing prompt fields (uses defaults) |
| `test_app_settings_from_yaml_empty` | Load empty/None YAML (uses all defaults) |
| `test_app_settings_from_yaml_invalid` | Load invalid YAML (returns defaults) |
| `test_app_settings_to_yaml` | Serialize model to YAML |

### Integration Tests

| Test Case | Description |
|-----------|-------------|
| Settings page load | Admin can view settings with prompt fields |
| Settings page save | Modified prompts persist to S3 |
| Chat mode switching | Correct prompt used for Tutor vs Answer mode |
| New user experience | First load without config.yaml uses defaults |

### Manual Testing Checklist

- [ ] Admin can access Settings page
- [ ] Settings page shows AI Model, Temperature, Whitelist fields
- [ ] Settings page shows Tutor Mode Prompt text area
- [ ] Settings page shows Answer Mode Prompt text area
- [ ] Saving settings persists all values to S3
- [ ] Chat in Tutor mode uses tutor_prompt
- [ ] Chat in Answer mode uses answer_prompt
- [ ] Non-admin cannot access Settings page
- [ ] App loads with missing/empty config.yaml (uses defaults)
- [ ] Prompts admin menu item is removed
- [ ] No errors in logs related to prompts.yaml

## Rollback Plan

1. **Revert code changes** - `git revert` the version commit
2. **Restore prompts.yaml** - Re-upload prompts.yaml to S3 bucket if deleted
3. **No database migration** - No database changes to rollback
4. **Config compatibility** - Old config.yaml format still works with rolled-back code

## References

- Requirements: `/workspaces/ist256-chatapp/docs/project_requirements.md` (v2.1.0 section)
- Current models: `/workspaces/ist256-chatapp/app/dal/models.py`
- Current settings: `/workspaces/ist256-chatapp/app/chat/settings.py`
- Current prompts: `/workspaces/ist256-chatapp/app/chat/prompts.py`

---

**Generated**: 2026-01-13
**Author**: AI-assisted design via /design command
**Version**: 2.1.0
**Status**: Implementation mostly complete as of 2026-01-13 - needs verification and documentation updates
