from loguru import logger
from streamlit_javascript import st_javascript
import hashlib
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
    # Create a MinIO client
    minio_client = Minio(
        minio_host_port,
        access_key=access_key,
        secret_key=secret_key,
        secure=False  # Set to False if not using HTTPS
    )

    # Specify the bucket and file to download

    # Download the file
    response = minio_client.get_object(bucket_name, object_key)
    file_content = response.read().decode('utf-8')
    emails = file_content.split(",")
    logger.info(f"email_count={len(emails)}, host={minio_host_port}, roster={object_key}")

    return emails


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