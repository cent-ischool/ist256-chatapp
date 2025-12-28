# Version Documentation Index

This directory contains detailed technical specifications and implementation plans for each version of the IST256 Chatapp.

## Version History

| Version | Release Date | Status | Features |
|---------|--------------|--------|----------|
| v2.0.1  | TBD | In Development | S3 config fallback error handling - graceful degradation when S3 unavailable |
| v2.0.0  | TBD | In Development | Production release: rename appnew.py to app.py, update deployment config, disable Streamlit email prompt |
| v1.0.10 | TBD | In Development | User preferences persistence (mode and context stored in database) |
| v1.0.9  | TBD | In Development | Admin UI option to export all chat logs in CSV or JSON format |
| v1.0.8  | TBD | In Development | UI polish, About/Help section, chat history download, enhanced error handling |
| v1.0.7  | TBD | In Development | Admin menu integration (Settings, Prompts, Session pages) |
| v1.0.6  | TBD | In Development | Chat logging to database with full metadata |
| v1.0.5  | TBD | In Development | Always-on context injection, personalized greeting |
| v1.0.4  | TBD | In Development | LLM Integration with mode-based prompts |
| v1.0.3  | TBD | In Development | Database & Logging Infrastructure for appnew.py |
| v1.0.2  | TBD | In Development | Authentication & Authorization for appnew.py |
| v1.0.1  | 2025-01-15   | Released | Session page, version tracking, UI footer display |

## Directory Structure

Each version has its own folder containing:
- `technical-spec.md` - Technical architecture and design decisions
- `implementation-plan.md` - Step-by-step implementation tasks

Example:
```
versions/
├── README.md (this file)
├── v1.0.1/
│   ├── technical-spec.md
│   └── implementation-plan.md
└── v1.0.2/
    ├── technical-spec.md
    └── implementation-plan.md
```

## Workflow

### 1. Add Requirements

Add feature requirements to `/docs/project_requirements.md`:

```markdown
## v1.0.2
**Status**: Planned
**Release Date**: TBD

### Features
- Feature 1 description
- Feature 2 description

### Technical Notes
- Any technical considerations
```

### 2. Generate Design Documentation

Run the `/design` command in Claude Code:

```
/design 1.0.2
```

This will:
- Parse requirements from project_requirements.md
- Analyze the codebase
- Generate technical-spec.md and implementation-plan.md
- Update VERSION in app/chat/constants.py
- Update this README with the new version

### 3. Review and Refine

- Navigate to `docs/versions/v1.0.2/`
- Review technical-spec.md for accuracy
- Review implementation-plan.md for completeness
- Refine as needed (AI is a starting point, not final authority)

### 4. Implement

- Create feature branch: `git checkout -b feature/v1.0.2-[feature-name]`
- Follow the implementation plan phase by phase
- Check off tasks as completed
- Update TODO.txt with progress

### 5. Deploy

- Commit changes
- Create PR referencing version docs
- Merge when approved
- Update this README with release date and status

## Version Naming Convention

We follow [semantic versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR** (x.0.0): Breaking changes to APIs or architecture
- **MINOR** (1.x.0): New features, backward compatible
- **PATCH** (1.0.x): Bug fixes, minor improvements

## Version States

- **Planned**: Requirements defined, design not yet started
- **In Development**: Design docs created, implementation in progress
- **Testing**: Implementation complete, testing in progress
- **Released**: Deployed to production

## Related Files

- High-level requirements: `/docs/project_requirements.md`
- Version constant: `/app/chat/constants.py`
- Task tracking: `/TODO.txt`
- Developer guide: `/CLAUDE.md`

## Utility Scripts

Use the version manager script for version operations:

```bash
# Show current version
python scripts/version_manager.py current

# List all documented versions
python scripts/version_manager.py list

# Validate version has complete docs
python scripts/version_manager.py validate 1.0.2

# Update version constant
python scripts/version_manager.py set 1.0.2
```

## Best Practices

1. **Always start with requirements** - Add to project_requirements.md before running /design
2. **Review AI output** - AI-generated docs are starting points, refine with domain knowledge
3. **Keep specs updated** - If implementation diverges from spec, update the spec
4. **Document decisions** - Use technical-spec.md to explain why choices were made
5. **Link to code** - Reference specific file paths and line numbers in docs
6. **Freeze released versions** - Don't modify docs for released versions, create new patch versions instead

## Future Enhancements

Ideas for improving the version management system:

- Automated changelog generation from version docs
- Git tag creation automation
- Version comparison tool (`version_manager.py diff 1.0.1 1.0.2`)
- Migration guide templates for breaking changes
- API documentation generation from specs
