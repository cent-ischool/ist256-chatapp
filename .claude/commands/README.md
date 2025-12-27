# Custom Claude Code Commands

This directory contains custom slash commands for the IST256 Chatapp project.

## Available Commands

### `/design [VERSION]`

**Purpose**: Automate the generation of technical specifications and implementation plans for a new version.

**Usage**:
```
/design 1.0.2
```

**What it does**:
1. Reads requirements from `docs/project_requirements.md` for the specified version
2. Analyzes the codebase using knowledge from `CLAUDE.md`
3. Generates `technical-spec.md` in `docs/versions/v[VERSION]/`
4. Generates `implementation-plan.md` in `docs/versions/v[VERSION]/`
5. Updates `VERSION` constant in `app/chat/constants.py`
6. Updates version tracking table in `docs/versions/README.md`
7. Provides a summary with next steps

**Prerequisites**:
- Version requirements must exist in `docs/project_requirements.md`
- Requirements should follow the format:
  ```markdown
  ## v[VERSION]
  **Status**: Planned
  **Release Date**: TBD

  ### Features
  - Feature 1 description
  - Feature 2 description

  ### Technical Notes
  - Technical considerations
  ```

**Outputs**:
- `/docs/versions/v[VERSION]/technical-spec.md` - Complete technical specification
- `/docs/versions/v[VERSION]/implementation-plan.md` - Phased implementation plan
- Updated `/app/chat/constants.py` - VERSION constant set to new version
- Updated `/docs/versions/README.md` - Version added to history table

**Example Workflow**:

1. Add requirements to `docs/project_requirements.md`
2. Run `/design 1.0.2`
3. Review generated documentation
4. Refine based on domain knowledge
5. Create feature branch and implement
6. Commit when ready (manual git operation)

## Related Documentation

- Version management guide: `/docs/versions/README.md`
- Project requirements: `/docs/project_requirements.md`
- Developer guide: `/CLAUDE.md`
- Templates:
  - Technical spec template: `/docs/templates/technical-spec-template.md`
  - Implementation plan template: `/docs/templates/implementation-plan-template.md`

## Utility Scripts

For manual version operations, use the version manager script:

```bash
# Show current version
python scripts/version_manager.py current

# List all documented versions
python scripts/version_manager.py list

# Validate version has complete docs
python scripts/version_manager.py validate 1.0.2

# Update version constant manually
python scripts/version_manager.py set 1.0.2
```
