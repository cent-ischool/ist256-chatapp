# Technical Specification: Chat Log Export - v1.0.9

## Overview

This feature adds an admin-only page that allows administrators to export all chat logs from the PostgreSQL database in either CSV or JSON format. The export includes a timestamp in the filename for easy identification and tracking. The page will be accessible only to admin users and will be positioned in the admin menu between "Prompts" and "Session".

## Architecture Changes

### Components Affected

- `/workspaces/ist256-chatapp/app/chat/appnew.py` (lines 67+)
  - Add "Export" menu item to admin sidebar navigation
  - Add page routing logic for the export page

### New Components

- `/workspaces/ist256-chatapp/app/chat/export.py`
  - New admin page module for chat log export functionality
  - Functions: `show_export()`, `export_logs_to_csv()`, `export_logs_to_json()`

### Dependencies

**External Libraries** (already in requirements.txt):
- `streamlit` - UI framework
- `sqlmodel` - ORM for database queries
- `pandas` - CSV/JSON export functionality
- `json` - JSON serialization (built-in)
- `datetime` - Timestamp generation (built-in)

**Internal Modules**:
- `dal.db.PostgresDb` - Database connection
- `dal.models.LogModel` - Chat log data model
- `constants` - Version constant update

## Data Models

### Database Changes

**No schema changes required.** The feature uses the existing `LogModel` table:

```python
class LogModel(SQLModel, table=True):
    __tablename__ = "logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    sessionid: str
    userid: str
    timestamp: str
    model: str
    rag: bool
    context: str
    role: str
    content: str
```

### API Changes

**No API changes.** This is a read-only export feature with no external API endpoints.

## Technical Design

### Backend Implementation

**Database Query Strategy:**
```python
# Query all logs ordered by timestamp
from sqlmodel import select
from dal.models import LogModel

def fetch_all_logs(db: PostgresDb) -> List[LogModel]:
    with db.get_session() as session:
        statement = select(LogModel).order_by(LogModel.timestamp)
        results = session.exec(statement).all()
        return list(results)
```

**CSV Export Implementation:**
- Use `pandas.DataFrame` to convert LogModel list to DataFrame
- Use `DataFrame.to_csv()` to generate CSV string
- Use `st.download_button()` to provide download to user
- Filename format: `chat_logs_YYYY-MM-DD_HH-MM-SS.csv`

**JSON Export Implementation:**
- Convert LogModel objects to dictionaries using `.model_dump()`
- Serialize list of dicts to JSON using `json.dumps(indent=2)`
- Use `st.download_button()` to provide download to user
- Filename format: `chat_logs_YYYY-MM-DD_HH-MM-SS.json`

**Timestamp Generation:**
```python
from datetime import datetime

def generate_timestamp_filename(base: str, extension: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{base}_{now}.{extension}"
```

### Frontend Implementation

**Streamlit UI Components:**

```python
def show_export():
    st.title("Export Chat Logs")

    st.markdown("Export all chat logs from the database.")

    # Info section
    st.info("This export includes all chat messages from all users and sessions.")

    # Statistics display
    total_logs = get_log_count()
    st.metric("Total Log Entries", total_logs)

    # Export format selection
    export_format = st.radio(
        "Export Format",
        options=["CSV", "JSON"],
        horizontal=True
    )

    # Export button
    if st.button("Generate Export"):
        with st.spinner("Generating export..."):
            if export_format == "CSV":
                data, filename = export_logs_to_csv()
            else:
                data, filename = export_logs_to_json()

            st.download_button(
                label=f"Download {export_format}",
                data=data,
                file_name=filename,
                mime="text/csv" if export_format == "CSV" else "application/json"
            )
            st.success(f"Export generated successfully! Click above to download.")
```

**User Flow:**
1. Admin user navigates to sidebar
2. Expands "Admin" menu
3. Clicks "Export" (positioned between "Prompts" and "Session")
4. Views total log count on Export page
5. Selects export format (CSV or JSON)
6. Clicks "Generate Export" button
7. Downloads file via download button

### Integration Points

**PostgreSQL Integration:**
- Use existing `st.session_state.db` (PostgresDb instance)
- Query via SQLModel ORM using `select(LogModel)`
- Read-only operation, no database writes

**S3 Integration:**
- None required (export is direct download, not stored in S3)

**Authentication/Authorization:**
- Access restricted to admin users only
- Use existing `st.session_state.validated == "admin"` check
- Menu item only visible to admins

**Session State:**
- `st.session_state.db` - PostgresDb instance (already initialized in v1.0.3)
- No new session state variables needed

## Configuration

### Environment Variables

**No new environment variables required.**

All necessary environment variables already exist:
- `DATABASE_URL` - PostgreSQL connection string (required)

### Config Files

**Updates Required:**

**1. `/workspaces/ist256-chatapp/app/chat/constants.py`**
```python
VERSION="1.0.9"  # Update from "1.0.8"
```

**No changes to:**
- `config.yaml` - No configuration needed
- `prompts.yaml` - No new prompts needed

## Security Considerations

### Authentication Requirements

- **Admin-only access:** Only users with `st.session_state.validated == "admin"` can see/access the Export page
- Menu item hidden from non-admin users
- Page should verify admin status at render time (defensive check)

### Authorization/Access Control

```python
def show_export():
    # Defensive check
    if st.session_state.get("validated") != "admin":
        st.error("Unauthorized access. Admin privileges required.")
        st.stop()
    # ... rest of implementation
```

### Data Privacy Concerns

- **Sensitive data exposure:** Chat logs contain user emails, prompts, and AI responses
- Export should only be available to authorized admins
- Downloaded file contains PII (userid/email)
- Admin responsibility: Secure handling of exported data
- No encryption on export (admin responsible for secure storage)

### Input Validation

- No user input required (read-only operation)
- Database query uses ORM (SQLModel), preventing SQL injection
- No user-provided filenames (generated automatically)

### SQL Injection Prevention

- Use SQLModel ORM for all queries (parameterized automatically)
- No raw SQL queries
- No user-provided WHERE clauses

### XSS Prevention

- No user-generated content rendered in HTML
- Streamlit components handle escaping automatically
- Export data is downloaded, not displayed in browser

## Performance Considerations

### Scalability Implications

**Current Scale:**
- Estimated logs: ~100-1000 messages per day in production
- Growth rate: Linear with user activity

**Performance Concerns:**
- Large exports (>10,000 rows) may cause memory issues
- Streamlit has 200MB file size limit for `st.download_button`
- Database query may be slow for very large datasets

**Mitigation Strategies:**
1. **Pagination/Filtering (Future):** Add date range filter for large exports
2. **Streaming (Future):** Stream CSV rows instead of loading all into memory
3. **Background Jobs (Future):** Use async task for large exports, store in S3

**Acceptable for v1.0.9:**
- Assumption: <50,000 log entries (typical for one semester)
- Memory usage: ~5-10MB for 10,000 logs
- Query time: <5 seconds for 50,000 logs

### Caching Strategies

- No caching needed for export (always fetch fresh data)
- Consider caching log count for display (refresh on page load)

### Database Query Optimization

**Current Query:**
```python
statement = select(LogModel).order_by(LogModel.timestamp)
```

**Index Recommendations (Future):**
- Add index on `timestamp` column for faster ordering
- Not critical for v1.0.9 (small dataset)

### Memory Usage

**CSV Export:**
- LogModel objects → pandas DataFrame → CSV string
- Memory = 2x log data size during conversion
- Acceptable for <50,000 rows

**JSON Export:**
- LogModel objects → dict list → JSON string
- Memory = 2x log data size during conversion
- Acceptable for <50,000 rows

## Error Handling

### Expected Errors and Handling

**1. Database Connection Failure**
```python
try:
    logs = fetch_all_logs(st.session_state.db)
except Exception as e:
    st.error("Database connection failed. Please try again.")
    logger.error(f"Database error during export: {e}")
    st.stop()
```

**2. Empty Database**
```python
if len(logs) == 0:
    st.warning("No chat logs found in the database.")
    st.stop()
```

**3. Export Generation Failure**
```python
try:
    data = df.to_csv(index=False)
except Exception as e:
    st.error("Failed to generate export. Please contact support.")
    logger.error(f"CSV generation error: {e}")
    st.stop()
```

### User-Facing Error Messages

- **Database Error:** "Unable to connect to database. Please try again or contact support."
- **Empty Database:** "No chat logs available for export."
- **Export Error:** "Export generation failed. Please try again."
- **Unauthorized Access:** "Admin privileges required to access this page."

### Logging Requirements

Use `loguru.logger` for all errors:
```python
logger.info(f"Admin {userid} generated {format} export: {row_count} rows")
logger.error(f"Export failed for {userid}: {error}")
```

### Recovery Procedures

- User can retry export by clicking "Generate Export" again
- No persistent state changes (read-only operation)
- No rollback needed

## Testing Strategy

### Unit Tests

**Note:** No test suite currently exists. Manual testing required for v1.0.9.

**Recommended Tests (Future):**
1. `test_fetch_all_logs()` - Verify database query returns all logs
2. `test_export_logs_to_csv()` - Verify CSV format correctness
3. `test_export_logs_to_json()` - Verify JSON format correctness
4. `test_generate_timestamp_filename()` - Verify filename format

### Integration Tests

**Recommended Tests (Future):**
1. Test database connection via PostgresDb
2. Test LogModel query with 0, 1, 100, 10000 rows
3. Test CSV export with special characters in content
4. Test JSON export with unicode characters

### Manual Testing

**Admin User Testing:**
- [ ] Admin user can see "Export" menu item
- [ ] Admin user can access Export page
- [ ] Total log count displays correctly
- [ ] CSV export generates valid CSV file
- [ ] JSON export generates valid JSON file
- [ ] Filename includes correct timestamp
- [ ] Downloaded file contains expected data
- [ ] Downloaded file opens correctly in Excel (CSV) or text editor (JSON)

**Non-Admin User Testing:**
- [ ] Non-admin user cannot see "Export" menu item
- [ ] Direct URL access to export page is denied (if applicable)

**Edge Cases:**
- [ ] Export with 0 logs (empty database)
- [ ] Export with 1 log
- [ ] Export with 10,000+ logs (performance test)
- [ ] Export with special characters in content (quotes, commas, newlines)
- [ ] Export with unicode/emoji in content
- [ ] Export when database connection fails

**Browser Testing:**
- [ ] Chrome: CSV/JSON download works
- [ ] Firefox: CSV/JSON download works
- [ ] Safari: CSV/JSON download works
- [ ] Edge: CSV/JSON download works

## Rollback Plan

### How to Revert

**v1.0.9 is a low-risk additive feature. Rollback is simple:**

1. **Remove Export Menu Item:**
   - Edit `/workspaces/ist256-chatapp/app/chat/appnew.py`
   - Comment out or remove "Export" menu item and routing logic

2. **Delete Export Module:**
   - Remove `/workspaces/ist256-chatapp/app/chat/export.py`

3. **Revert Version Constant:**
   - Edit `/workspaces/ist256-chatapp/app/chat/constants.py`
   - Change `VERSION="1.0.9"` back to `VERSION="1.0.8"`

4. **Redeploy:**
   - Commit rollback changes
   - Push to main branch
   - CI/CD will auto-deploy

**No database rollback needed** (no schema changes).

**No configuration rollback needed** (no config changes).

### Verification After Rollback

- [ ] Export menu item no longer visible
- [ ] Application functions normally
- [ ] No errors in logs
- [ ] Version displays as "1.0.8"

## References

- **Related issues:** None (new feature)
- **Related PRs:** None (first implementation)
- **External docs:**
  - Streamlit download_button: https://docs.streamlit.io/library/api-reference/widgets/st.download_button
  - Pandas to_csv: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
  - SQLModel select: https://sqlmodel.tiangolo.com/tutorial/select/

---

**Generated**: 2025-12-27
**Author**: AI-assisted design via /design command
**Version**: v1.0.9
