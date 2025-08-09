from config.settings import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET,
)
import boto3
import os

storage_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)


def download_file(clientId, object_name, raw_file_path="/tmp/raw"):
    os.makedirs(raw_file_path, exist_ok=True)
    raw_media_path = f"{clientId}/raw/{object_name}"
    dest_path = f"{raw_file_path}/{object_name}"
    storage_client.download_file(MINIO_BUCKET, raw_media_path, dest_path)


def upload_file(clientId, local_path):
    remote_path = f"{clientId}/processed/{os.path.basename(local_path)}"
    storage_client.upload_file(local_path, MINIO_BUCKET, remote_path)


def upload_directory(clientId, processed_dir):
    media_id = os.path.basename(processed_dir.rstrip("/"))
    base_remote_dir = f"{clientId}/processed/{media_id}"

    for root, dirs, files in os.walk(processed_dir):
        for file in files:
            full_local_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_local_path, processed_dir)
            remote_path = os.path.join(base_remote_dir, relative_path).replace(
                "\\", "/"
            )

            storage_client.upload_file(full_local_path, MINIO_BUCKET, remote_path)
