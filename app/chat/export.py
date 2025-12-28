import os
import json
from datetime import datetime
from typing import List, Tuple
import streamlit as st
import pandas as pd
from loguru import logger
from sqlmodel import select

from dal.db import PostgresDb
from dal.models import LogModel


def generate_timestamp_filename(base: str, extension: str) -> str:
    """Generate filename with timestamp in format: base_YYYY-MM-DD_HH-MM-SS.ext"""
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{base}_{now}.{extension}"


def fetch_all_logs(db: PostgresDb) -> List[LogModel]:
    """Fetch all chat logs from database ordered by timestamp."""
    try:
        with db.get_session() as session:
            statement = select(LogModel).order_by(LogModel.timestamp)
            results = session.exec(statement).all()
            return list(results)
    except Exception as e:
        logger.error(f"Failed to fetch logs: {e}")
        raise


def get_log_count(db: PostgresDb) -> int:
    """Get total count of chat logs in database."""
    try:
        with db.get_session() as session:
            statement = select(LogModel)
            results = session.exec(statement).all()
            return len(list(results))
    except Exception as e:
        logger.error(f"Failed to count logs: {e}")
        raise


def export_logs_to_csv(logs: List[LogModel]) -> Tuple[str, str]:
    """Convert logs to CSV format.

    Returns:
        Tuple of (csv_data, filename)
    """
    try:
        # Convert to list of dicts
        data = [log.model_dump() for log in logs]
        # Create DataFrame
        df = pd.DataFrame(data)
        # Generate CSV
        csv_data = df.to_csv(index=False)
        # Generate filename
        filename = generate_timestamp_filename("chat_logs", "csv")
        return csv_data, filename
    except Exception as e:
        logger.error(f"Failed to generate CSV: {e}")
        raise


def export_logs_to_json(logs: List[LogModel]) -> Tuple[str, str]:
    """Convert logs to JSON format.

    Returns:
        Tuple of (json_data, filename)
    """
    try:
        # Convert to list of dicts
        data = [log.model_dump() for log in logs]
        # Serialize to JSON with indentation
        json_data = json.dumps(data, indent=2)
        # Generate filename
        filename = generate_timestamp_filename("chat_logs", "json")
        return json_data, filename
    except Exception as e:
        logger.error(f"Failed to generate JSON: {e}")
        raise


def show_export():
    """Render the Export page in Streamlit."""

    # Defensive admin check
    if st.session_state.get("validated") != "admin":
        st.error("Unauthorized access. Admin privileges required.")
        st.stop()

    st.title("Export Chat Logs")
    st.markdown("Export all chat logs from the database.")

    # Get database instance
    db = st.session_state.db

    # Display statistics
    try:
        log_count = get_log_count(db)
        st.metric("Total Log Entries", log_count)

        if log_count == 0:
            st.warning("No chat logs found in the database.")
            st.stop()
    except Exception as e:
        st.error("Unable to connect to database. Please try again.")
        logger.error(f"Database connection error: {e}")
        st.stop()

    # Export format selection
    st.subheader("Export Format")
    export_format = st.radio(
        "Choose format:",
        options=["CSV", "JSON"],
        horizontal=True,
        help="CSV for Excel/spreadsheets, JSON for programmatic access"
    )

    # Export button
    if st.button("Generate Export", type="primary"):
        with st.spinner(f"Generating {export_format} export..."):
            try:
                # Fetch all logs
                logs = fetch_all_logs(db)

                # Generate export
                if export_format == "CSV":
                    data, filename = export_logs_to_csv(logs)
                    mime_type = "text/csv"
                else:
                    data, filename = export_logs_to_json(logs)
                    mime_type = "application/json"

                # Log the export action
                userid = st.session_state.get("userid", "unknown")
                logger.info(f"Admin {userid} generated {export_format} export: {len(logs)} rows")

                # Provide download button
                st.download_button(
                    label=f"📥 Download {export_format}",
                    data=data,
                    file_name=filename,
                    mime=mime_type
                )
                st.success(f"Export generated successfully! Click above to download {filename}")

            except Exception as e:
                st.error("Failed to generate export. Please try again or contact support.")
                logger.error(f"Export generation failed: {e}")
