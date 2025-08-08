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


def download_file(clientId, objectName, raw_file_path="/tmp/raw"):
    os.makedirs(raw_file_path, exist_ok=True)
    raw_media_path = f"{clientId}/raw/{objectName}"
    dest_path = f"{raw_file_path}/{objectName}"
    storage_client.download_file(MINIO_BUCKET, raw_media_path, dest_path)
