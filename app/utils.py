from loguru import logger
from streamlit_javascript import st_javascript
import hashlib
import random
from time import sleep
from datetime import datetime
from minio import Minio
from typing import List


def hash_email_to_boolean(email: str) -> bool:
    '''
    Use md5 to get a random hash then map that to a boolean
    '''
    hashed = hashlib.md5(email.encode()).hexdigest()
    ascii_sum = sum(ord(c) for c in hashed)
    bool_hash =  ascii_sum % 2 == 0
    logger.info(f"email={email}, md5={hashed} ascii_sum={ascii_sum} even={bool_hash}")

    return bool_hash

def stream_text(text: str):
    """Streams text to the Streamlit chat message container."""
    def split_string_randomly(input_string):
        chunks = []
        while input_string:
            chunk_size = random.randint(2, 6)  # Random size between 2 and 5
            chunk = input_string[:chunk_size]  # Get the chunk
            chunks.append(chunk)  # Add it to the list
            input_string = input_string[chunk_size:]  # Remove the chunk from the input string
        return chunks
    for chunk in split_string_randomly(text):
        yield chunk
        sleep(random.uniform(0.01, 0.1))  # Simulate streaming delay

def generate_chat_history_export(session_state) -> str:
    """
    Generates a formatted text export of the current chat session.

    Args:
        session_state: Streamlit session state object containing chat data

    Returns:
        Formatted string with session metadata and conversation history
    """
    lines = []
    lines.append("=" * 60)
    lines.append("IST256 AI Chat History")
    lines.append("=" * 60)
    lines.append(f"Session ID: {session_state.sessionid}")
    lines.append(f"User: {session_state.auth_model.email}")
    lines.append(f"Mode: {session_state.mode}")
    lines.append(f"Context: {session_state.context}")
    lines.append(f"Model: {session_state.config.ai_model}")
    lines.append(f"Export Time: {datetime.now().isoformat()}")
    lines.append("=" * 60)
    lines.append("")

    for idx, message in enumerate(session_state.messages, 1):
        role = message["role"].upper()
        content = message["content"]
        lines.append(f"[{idx}] {role}:")
        lines.append(content)
        lines.append("")
        lines.append("-" * 60)
        lines.append("")

    return "\n".join(lines)

def generate_all_chats_export(db, email: str) -> str:
    """
    Generates a formatted text export of all chat sessions for the current user.
    Queries the database to get all messages for this user.

    Args:
        db: PostgreSQL database connection object
        email: User's email address

    Returns:
        Formatted string with all chat sessions grouped by session ID
    """
    try:
        from sqlmodel import select
        from dal.models import LogModel

        # Query database for all user's messages using SQLModel
        with db.get_session() as session:
            statement = select(LogModel).where(
                LogModel.userid == email
            ).order_by(LogModel.timestamp)

            results = session.exec(statement).all()

        if not results:
            return "No chat history found for this user."

        lines = []
        lines.append("=" * 60)
        lines.append("IST256 AI - Complete Chat History")
        lines.append("=" * 60)
        lines.append(f"User: {email}")
        lines.append(f"Export Time: {datetime.now().isoformat()}")
        lines.append(f"Total Messages: {len(results)}")
        lines.append("=" * 60)
        lines.append("")

        # Group messages by session
        current_session = None
        message_num = 0

        for log in results:
            # New session header
            if log.sessionid != current_session:
                if current_session is not None:
                    lines.append("")
                    lines.append("=" * 60)
                    lines.append("")

                current_session = log.sessionid
                message_num = 0
                lines.append(f"SESSION: {log.sessionid}")
                lines.append(f"Started: {log.timestamp}")
                lines.append(f"Model: {log.model}")
                lines.append(f"Context: {log.context}")
                lines.append("-" * 60)
                lines.append("")

            # Message content
            message_num += 1
            lines.append(f"[{message_num}] {log.role.upper()}:")
            lines.append(log.content)
            lines.append("")

        lines.append("")
        lines.append("=" * 60)
        lines.append("End of Chat History")
        lines.append("=" * 60)

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"Failed to generate all chats export: user={email}, error={e}")
        return f"Error generating chat history: {str(e)}"

def get_parent_url():
    url = st_javascript("await fetch('').then(r => window.parent.location.href)")
    return url


def get_roster(
    minio_host_port: str,
    access_key: str,
    secret_key: str,
    bucket_name: str,
    object_key: str
    ) -> List[str]:
    """
    Fetch whitelist file from S3 and return list of email addresses.

    Note: Function name is 'get_roster' for backwards compatibility,
    but it fetches the whitelist file specified in config.whitelist.

    Args:
        minio_host_port: MinIO host and port (e.g., "host:9000")
        access_key: S3 access key
        secret_key: S3 secret key
        bucket_name: S3 bucket name
        object_key: Object key (whitelist file path) in bucket

    Returns:
        List of email addresses from whitelist file, or empty list if fetch fails
    """
    try:
        # Create a MinIO client
        minio_client = Minio(
            minio_host_port,
            access_key=access_key,
            secret_key=secret_key,
            secure=False  # Set to False if not using HTTPS
        )

        # Download the file
        response = minio_client.get_object(bucket_name, object_key)
        file_content = response.read().decode('utf-8')
        emails = file_content.split(",")
        logger.info(f"email_count={len(emails)}, host={minio_host_port}, whitelist={object_key}")

        return emails
    except Exception as e:
        logger.error(f"Failed to fetch whitelist from s3://{bucket_name}/{object_key}: {e}")
        logger.warning("Returning empty whitelist - all users will be denied access unless in exception list")
        return []


if __name__ == "__main__":
    import os
    emails = get_roster(
        minio_host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        bucket_name=os.environ["S3_BUCKET"],
        object_key=os.environ["ROSTER_FILE"]
        )
    print(emails)