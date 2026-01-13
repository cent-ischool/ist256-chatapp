import os
import streamlit as st
from dal.s3 import get_roster


def show_session():
    """Display session variables and user permission information."""
    st.title("Session Debug & User Permissions")

    # Permission Information Section
    st.header("👥 User Permissions")

    # Load permission lists
    admin_users = [user.lower().strip() for user in os.environ.get("ADMIN_USERS", "").split(",") if user.strip()]
    exception_users = [user.lower().strip() for user in os.environ.get("ROSTER_EXCEPTION_USERS", "").split(",") if user.strip()]

    try:
        roster_users = [user.lower().strip() for user in get_roster(
            os.environ["S3_HOST"],
            os.environ["S3_ACCESS_KEY"],
            os.environ["S3_SECRET_KEY"],
            os.environ["S3_BUCKET"],
            os.environ["ROSTER_FILE"]
        ) if user.strip()]
    except Exception as e:
        st.error(f"Failed to load roster: {e}")
        roster_users = []

    # Display current user's permission level
    if 'auth_model' in st.session_state:
        current_email = st.session_state.auth_model.email
        if 'validated' in st.session_state:
            user_type = st.session_state.validated
            st.success(f"Current User: **{current_email}** (Permission: **{user_type}**)")

    # Admin Users Section
    with st.expander(f"🔐 Admin Users ({len(admin_users)})", expanded=True):
        st.markdown("**Source:** `ADMIN_USERS` environment variable")
        st.markdown("**Access:** Full admin access (Settings, Export, Roster, Session pages)")
        if admin_users:
            for email in admin_users:
                st.text(f"• {email}")
        else:
            st.info("No admin users configured")

    # Exception Users Section
    with st.expander(f"⚡ Exception Users ({len(exception_users)})", expanded=False):
        st.markdown("**Source:** `ROSTER_EXCEPTION_USERS` environment variable")
        st.markdown("**Access:** Bypass roster check, chat access only (no admin pages)")
        if exception_users:
            for email in exception_users:
                st.text(f"• {email}")
        else:
            st.info("No exception users configured")

    # Roster Users Section
    with st.expander(f"📋 Roster Users ({len(roster_users)})", expanded=False):
        st.markdown(f"**Source:** `{os.environ.get('ROSTER_FILE', 'roster.txt')}` in MinIO S3")
        st.markdown("**Access:** Standard chat access (no admin pages)")
        if roster_users:
            # Show first 50, with option to see all
            display_count = 50
            for email in roster_users[:display_count]:
                st.text(f"• {email}")
            if len(roster_users) > display_count:
                if st.button(f"Show all {len(roster_users)} emails"):
                    for email in roster_users[display_count:]:
                        st.text(f"• {email}")
        else:
            st.info("No roster users found (empty roster)")

    # Authorization Logic Reference
    with st.expander("ℹ️ Authorization Logic", expanded=False):
        st.markdown("""
        **User authentication and authorization follows this order:**

        1. User logs in via Azure AD (MSAL)
        2. Email extracted from authentication token
        3. Authorization check (in order):
           - If email in **Admin Users** → Grant admin access
           - Else if email in **Exception Users** → Grant chat access
           - Else if email in **Roster Users** → Grant chat access
           - Else → **Deny access** (show unauthorized message)

        **Note:** Admin users have full access including admin pages. Exception and Roster users have chat access only.
        """)

    # Session State Section
    st.header("🔍 Session State Variables")
    st.markdown("**Current Streamlit session state:**")
    st.json({k: str(v) for k, v in st.session_state.items()})
