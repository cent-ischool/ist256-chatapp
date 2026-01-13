import os
import streamlit as st
from loguru import logger

from dal.s3 import S3Client


def show_whitelist():
    """Render the Whitelist management page in Streamlit."""
    s3client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )

    st.title("Whitelist Management")
    st.markdown("Manage the whitelist of authorized users.")

    # Get whitelist filename from config
    whitelist_file = st.session_state.config.whitelist if st.session_state.config.whitelist else "whitelist.txt"

    # Display whitelist filename
    st.info(f"**Whitelist File:** `{whitelist_file}`")

    # Load current whitelist from S3
    try:
        current_whitelist_text = s3client.get_text_file(
            os.environ["S3_BUCKET"],
            whitelist_file
        )
        emails = [email.strip() for email in current_whitelist_text.split(",") if email.strip()]
        logger.info(f"Loaded whitelist from S3: {len(emails)} emails")
    except Exception as e:
        st.error(f"Failed to load whitelist from S3: {e}")
        logger.error(f"Failed to load whitelist: {e}")
        emails = []
        current_whitelist_text = ""

    # Display stats
    st.metric("Total Emails in Whitelist", len(emails))

    # Editable text area
    st.header("Edit Whitelist")
    st.markdown("""
    **Instructions:**
    - Enter one email per line or comma-separated
    - Emails will be normalized (trimmed, lowercased) on save
    - Empty lines will be ignored
    """)

    whitelist_input = st.text_area(
        "Whitelist Emails",
        value="\n".join(emails),  # Display one per line for readability
        height=300,
        help="List of authorized email addresses, one per line"
    )

    # Save button
    col1, col2 = st.columns([1, 3])
    with col1:
        save_button = st.button("💾 Save Whitelist", type="primary")
    with col2:
        if st.button("🔄 Reset to Current"):
            st.rerun()

    if save_button:
        try:
            # Parse input (handle both newline and comma separated)
            input_text = whitelist_input.replace("\n", ",")
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
            s3client.put_whitelist(
                os.environ["S3_BUCKET"],
                whitelist_file,
                unique_emails
            )

            st.success(f"✅ Whitelist saved successfully! Total emails: {len(unique_emails)}")
            logger.info(f"Admin {st.session_state.auth_model.email} saved whitelist with {len(unique_emails)} emails")

            # Show diff if changed
            if len(unique_emails) != len(emails):
                st.info(f"Email count changed: {len(emails)} → {len(unique_emails)}")

        except Exception as e:
            st.error(f"Failed to save whitelist: {e}")
            logger.error(f"Failed to save whitelist: {e}", exc_info=True)
