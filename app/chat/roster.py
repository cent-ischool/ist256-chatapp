import os
import streamlit as st
from loguru import logger

from dal.s3 import S3Client


def show_roster():
    """Render the Roster management page in Streamlit."""
    s3client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )

    st.title("Roster Management")
    st.markdown("Manage the whitelist of authorized users (roster).")

    # Load current roster from S3
    try:
        current_roster_text = s3client.get_text_file(
            os.environ["S3_BUCKET"],
            os.environ["ROSTER_FILE"]
        )
        emails = [email.strip() for email in current_roster_text.split(",") if email.strip()]
        logger.info(f"Loaded roster from S3: {len(emails)} emails")
    except Exception as e:
        st.error(f"Failed to load roster from S3: {e}")
        logger.error(f"Failed to load roster: {e}")
        emails = []
        current_roster_text = ""

    # Display stats
    st.metric("Total Emails in Roster", len(emails))

    # Editable text area
    st.header("Edit Roster")
    st.markdown("""
    **Instructions:**
    - Enter one email per line or comma-separated
    - Emails will be normalized (trimmed, lowercased) on save
    - Empty lines will be ignored
    """)

    roster_input = st.text_area(
        "Roster Emails",
        value="\n".join(emails),  # Display one per line for readability
        height=300,
        help="List of authorized email addresses, one per line"
    )

    # Save button
    col1, col2 = st.columns([1, 3])
    with col1:
        save_button = st.button("💾 Save Roster", type="primary")
    with col2:
        if st.button("🔄 Reset to Current"):
            st.rerun()

    if save_button:
        try:
            # Parse input (handle both newline and comma separated)
            input_text = roster_input.replace("\n", ",")
            new_emails = [email.strip().lower() for email in input_text.split(",") if email.strip()]

            # Remove duplicates while preserving order
            seen = set()
            unique_emails = []
            for email in new_emails:
                if email not in seen:
                    seen.add(email)
                    unique_emails.append(email)

            # Validate emails (basic check)
            invalid_emails = [e for e in unique_emails if "@" not in e or "." not in e]
            if invalid_emails:
                st.warning(f"Warning: {len(invalid_emails)} potentially invalid emails detected")
                with st.expander("Show invalid emails"):
                    st.write(invalid_emails)

            # Save to S3
            s3client.put_roster(
                os.environ["S3_BUCKET"],
                os.environ["ROSTER_FILE"],
                unique_emails
            )

            st.success(f"✅ Roster saved successfully! Total emails: {len(unique_emails)}")
            logger.info(f"Admin {st.session_state.auth_model.email} saved roster with {len(unique_emails)} emails")

            # Show diff if changed
            if len(unique_emails) != len(emails):
                st.info(f"Email count changed: {len(emails)} → {len(unique_emails)}")

        except Exception as e:
            st.error(f"Failed to save roster: {e}")
            logger.error(f"Failed to save roster: {e}", exc_info=True)
