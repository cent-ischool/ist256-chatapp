---
description: Generate technical specifications and implementation plans for a new version
---

# Design Command

You are generating design documentation for IST256 Chatapp version $ARGUMENTS.

## Task: Generate Version Documentation

**Version**: $ARGUMENTS

### Step 1: Parse Requirements

1. Read `/workspaces/ist256-chatapp/docs/project_requirements.md`
2. Search for the section header `## v$ARGUMENTS` or `## $ARGUMENTS`
3. Extract all content under that version section until the next version header
4. If no section found, inform the user: "No requirements found for version $ARGUMENTS in project_requirements.md. Please add requirements first."
5. Parse out:
   - Features list
   - Technical notes
   - Any constraints or dependencies mentioned

### Step 2: Analyze Codebase

Based on the extracted requirements, use your knowledge from `/workspaces/ist256-chatapp/CLAUDE.md` to analyze:

1. **Existing patterns to follow:**
   - Authentication patterns (Azure AD via MSAL)
   - Configuration management (MinIO S3 for config.yaml, prompts.yaml)
   - Database patterns (PostgreSQL with SQLModel)
   - LLM integration patterns (AzureOpenAILLM, OllamaLLM)
   - Streamlit UI patterns in app/chat/

2. **Files that will need modification:**
   - Which existing files in app/chat/, app/llm/, app/dal/ are affected?
   - Identify exact file paths

3. **New files needed:**
   - What new Python modules or pages are required?
   - What new configuration entries are needed?

4. **Database implications:**
   - Any schema changes to LogModel or new models needed?
   - Migration requirements?

5. **Security considerations:**
   - Authentication/authorization requirements
   - Access control (admin vs roster vs exception users)
   - Data validation needs

6. **Integration points:**
   - MinIO S3 integration for config/data
   - PostgreSQL for logging
   - Azure OpenAI or Ollama for LLM
   - Streamlit session state management

### Step 3: Generate Technical Specification

1. Read template from `/workspaces/ist256-chatapp/docs/templates/technical-spec-template.md`
2. Create directory: `/workspaces/ist256-chatapp/docs/versions/v$ARGUMENTS/`
3. Generate comprehensive technical specification by filling in the template:

   **Overview**: Summarize the features from requirements

   **Architecture Changes**:
   - Components Affected: List specific files with absolute paths
   - New Components: List new files to create with absolute paths
   - Dependencies: Libraries or modules required

   **Data Models**:
   - Database Changes: Schema modifications if any
   - API Changes: New endpoints or function signatures

   **Technical Design**:
   - Backend Implementation: Detailed approach using existing patterns
   - Frontend Implementation: Streamlit components and UI flow
   - Integration Points: How it connects to S3, DB, LLM, auth

   **Configuration**:
   - Environment Variables: Any new or modified env vars
   - Config Files: Changes to config.yaml, prompts.yaml, constants.py

   **Security Considerations**:
   - Authentication requirements
   - Authorization/access control
   - Data validation
   - SQL injection prevention
   - XSS prevention

   **Performance Considerations**:
   - Scalability implications
   - Caching strategies
   - Database query optimization

   **Error Handling**:
   - Expected errors and handling
   - User-facing error messages
   - Logging requirements

   **Testing Strategy**:
   - Unit test cases
   - Integration test scenarios
   - Manual testing steps (admin vs non-admin, edge cases)

   **Rollback Plan**:
   - How to revert if issues arise

4. Save to: `/workspaces/ist256-chatapp/docs/versions/v$ARGUMENTS/technical-spec.md`

### Step 4: Generate Implementation Plan

1. Read template from `/workspaces/ist256-chatapp/docs/templates/implementation-plan-template.md`
2. Generate detailed implementation plan by filling in the template:

   **Timeline**: Estimate effort based on complexity (Low/Medium/High)

   **Phase 1: Preparation**:
   - Review technical specification
   - Set up development branch
   - Update TODO.txt
   - Verify dependencies

   **Phase 2: Backend Implementation**:
   - Specific tasks broken down from technical spec
   - Files to Modify: Absolute paths with description of changes
   - Files to Create: Absolute paths with purpose

   **Phase 3: Frontend Implementation**:
   - Specific UI tasks
   - Streamlit component additions
   - Files to modify in app/chat/

   **Phase 4: Configuration & Constants**:
   - Update VERSION = "$ARGUMENTS" in app/chat/constants.py
   - Update config files
   - Add new constants

   **Phase 5: Testing**:
   - Manual testing checklist with specific test cases
   - Integration testing (DB, S3, LLM)
   - Admin vs non-admin user testing

   **Phase 6: Documentation**:
   - Update CLAUDE.md if architecture changes
   - Update README.md if user-facing changes
   - Add inline code comments

   **Phase 7: Deployment**:
   - Commit message format
   - PR creation
   - Code review
   - Merge and monitor

   **Dependencies**: List any blockers

   **Risks & Mitigation**: Identify potential issues

   **Success Criteria**: Specific, measurable outcomes

3. Save to: `/workspaces/ist256-chatapp/docs/versions/v$ARGUMENTS/implementation-plan.md`

### Step 5: Update Version Constant

1. Read current contents of `/workspaces/ist256-chatapp/app/chat/constants.py`
2. Update the VERSION constant on line 1 to: `VERSION="$ARGUMENTS"`
3. Keep all other content unchanged
4. Write the file back
5. Confirm the change: "Updated VERSION to $ARGUMENTS in app/chat/constants.py"

### Step 6: Update Version Index

1. Read `/workspaces/ist256-chatapp/docs/versions/README.md`
2. Find the version history table
3. Add new row to the table:
   ```
   | v$ARGUMENTS | TBD | In Development | [Features from requirements] |
   ```
4. Insert in version order (latest first)
5. Write the file back

### Step 7: Provide Summary

Generate a summary for the user with this information:

```
Version Design Complete: v$ARGUMENTS

Generated Documentation:
- Technical Specification: /workspaces/ist256-chatapp/docs/versions/v$ARGUMENTS/technical-spec.md
- Implementation Plan: /workspaces/ist256-chatapp/docs/versions/v$ARGUMENTS/implementation-plan.md

Updated Files:
- VERSION constant: app/chat/constants.py (now v$ARGUMENTS)
- Version index: docs/versions/README.md

Features Included:
[List features from requirements]

Files to Modify:
- [Count] existing files

Files to Create:
- [Count] new files

Estimated Complexity: [Low/Medium/High]

Next Steps:
1. Review technical-spec.md for accuracy
2. Review implementation-plan.md for completeness
3. Refine as needed based on domain knowledge
4. Create feature branch: git checkout -b feature/v$ARGUMENTS-[feature-name]
5. Follow implementation plan phase by phase
6. Commit when ready (manual git operation)
```

## Important Guidelines

### Use Absolute Paths
All file paths must be absolute starting with `/workspaces/ist256-chatapp/`

### Follow Existing Patterns
Reference CLAUDE.md to understand:
- How authentication works (Azure AD MSAL)
- How config is stored (MinIO S3)
- How database logging works (PostgreSQL with ChatLogger)
- How LLM APIs are integrated (LLMBase strategy pattern)
- How Streamlit session state is managed

### Be Specific and Actionable
- Don't write "update the settings page" - write "modify app/chat/settings.py to add temperature slider using st.slider()"
- Don't write "add database support" - write "add temperature field to ConfigurationModel in app/dal/models.py"
- Include specific Streamlit component names (st.slider, st.selectbox, etc.)
- Include specific file paths and line number ranges where possible

### Consider Integration
Every feature should address:
- How it integrates with existing auth (admin vs roster users)
- How it persists data (MinIO S3, PostgreSQL, or session state)
- How it interacts with LLM if applicable
- How it handles errors and logs

### Security First
Always consider:
- Who can access this feature? (Admin only? All users?)
- What input validation is needed?
- How to prevent SQL injection, XSS?
- What sensitive data is involved?

### No Git Automation
Do NOT execute any git commands. The user will manually:
- Create feature branches
- Commit changes
- Create pull requests
- Merge to main

## Error Handling

If requirements not found:
```
Error: No requirements found for version $ARGUMENTS

Please add requirements to docs/project_requirements.md first:

## v$ARGUMENTS
**Status**: Planned
**Release Date**: TBD

### Features
- Feature 1
- Feature 2

### Technical Notes
- Technical considerations

Then run /design $ARGUMENTS again.
```

If directory creation fails:
```
Error: Could not create directory docs/versions/v$ARGUMENTS/
Please check file permissions.
```

## Example Usage

```
/design 1.0.2
```

This will generate complete design documentation for version 1.0.2 based on requirements in project_requirements.md.

---

**Note**: This command uses AI to generate design documentation. Always review and refine the output based on your domain expertise. AI provides a strong starting point but human validation is essential.
