from loguru import logger
from minio import Minio
from typing import List
import io


class S3Client:
    def __init__(self, host_port: str, access_key: str, secret_key: str, secure: bool = False):
        self.client = Minio(
            host_port,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        logger.info(f"S3Client initialized for host={host_port}")

    def download_file(self, bucket_name: str, object_key: str, dest_path: str):
        response = self.client.get_object(bucket_name, object_key)
        with open(dest_path, 'wb') as file_data:
            for d in response.stream(32*1024):
                file_data.write(d)
        logger.info(f"Downloaded s3://{bucket_name}/{object_key} to {dest_path}")

    def file_exists(self, bucket_name: str, object_key: str) -> bool:
        try:
            self.client.stat_object(bucket_name, object_key)
            logger.info(f"File exists: s3://{bucket_name}/{object_key}")
            return True
        except Exception as e:
            logger.warning(f"File does not exist: s3://{bucket_name}/{object_key}, error={e}")
            return False

    def get_text_file(self, bucket_name: str, object_key: str) -> str:
        response = self.client.get_object(bucket_name, object_key)
        file_content = response.read().decode('utf-8')
        logger.info(f"Fetched text file s3://{bucket_name}/{object_key}, size={len(file_content)} characters")
        return file_content
    
    def put_text_file(self, bucket_name: str, object_key: str, content: str):
        # Minio expects a file-like object (with .read()) for data. Wrap bytes in BytesIO.
        if isinstance(content, str):
            content_bytes = content.encode('utf-8')
        else:
            # If content is already bytes-like, accept it
            content_bytes = content

        data = io.BytesIO(content_bytes)
        byte_length = len(content_bytes)

        self.client.put_object(
            bucket_name,
            object_key,
            data=data,
            length=byte_length,
            content_type='text/plain'
        )
        logger.info(f"Uploaded text file to s3://{bucket_name}/{object_key}, size={len(content)} characters")   

    def list_objects(self, bucket_name: str, prefix: str = '') -> List[str]:
        objects = self.client.list_objects(bucket_name, prefix=prefix)
        object_keys = [obj.object_name for obj in objects]
        logger.info(f"Listed {len(object_keys)} objects in s3://{bucket_name}/{prefix}")
        return object_keys
    

# Leggacy function for getting roster
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
    import yaml
    emails = get_roster(
        minio_host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        bucket_name=os.environ["S3_BUCKET"],
        object_key=os.environ["ROSTER_FILE"]
        )
    print(emails)

    s3client = S3Client(
        host_port=os.environ["S3_HOST"],
        access_key=os.environ["S3_ACCESS_KEY"],
        secret_key=os.environ["S3_SECRET_KEY"],
        secure=False
    )
    if s3client.file_exists(os.environ["S3_BUCKET"], os.environ["CONFIG_FILE"]):
        content = s3client.get_text_file(os.environ["S3_BUCKET"], os.environ["CONFIG_FILE"])
        print(content)
    else:
        config = yaml.safe_load(open("data/config.yaml", 'r'))
        s3client.put_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"], yaml.dump(config))

    if s3client.file_exists(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"]):
        content = s3client.get_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"])
        print(content)
    else:
        config = yaml.safe_load(open("data/prompts.yaml", 'r'))
        s3client.put_text_file(os.environ["S3_BUCKET"], os.environ["PROMPTS_FILE"], yaml.dump(config))
    