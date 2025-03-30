import asyncio
import io
import logging
from datetime import timedelta

from minio import Minio

from config import Config


class StorageService:
    # TODO: Error handling, Retry logic, etc.

    def __init__(self):
        """Initialize the MinIO client and ensure the bucket exists."""
        logging.info('Initializing StorageService')
        self.minio_client = Minio(
            Config.MINIO_ENDPOINT,
            access_key=Config.MINIO_ACCESS_KEY,
            secret_key=Config.MINIO_SECRET_KEY,
            secure=Config.MINIO_SECURE,
        )
        self.bucket_name = Config.MINIO_BUCKET_NAME
        self.ensure_bucket_exists()
        self.presigned_url_expires_in = timedelta(
            seconds=Config.MINIO_PRESIGNED_URL_EXPIRES_IN_SECONDS
        )

    def ensure_bucket_exists(self):
        """Check if the bucket exists, and create it if it does not."""
        if not self.minio_client.bucket_exists(self.bucket_name):
            self.minio_client.make_bucket(self.bucket_name)

    def upload_binary(
        self,
        data: bytes,
        object_name: str,
        content_type: str = 'application/octet-stream',
    ):
        """Upload binary data to the bucket."""
        binary_stream = io.BytesIO(data)
        self.minio_client.put_object(
            self.bucket_name,
            object_name=object_name,
            data=binary_stream,
            length=len(data),
            content_type=content_type,
        )

    def get_public_url(self, object_name: str) -> str:
        """Get the public URL of the object."""
        return self.minio_client.presigned_get_object(
            self.bucket_name,
            object_name=object_name,
            expires=self.presigned_url_expires_in,
        )

    async def upload_binary_async(
        self, data: bytes, object_name: str, content_type: str | None = None
    ):
        """Upload binary data to the bucket (async version)."""
        if not content_type:
            content_type = 'application/octet-stream'
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, self.upload_binary, data, object_name, content_type
        )

    async def get_public_url_async(self, object_name: str) -> str:
        """Get the public URL of the object (async version)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_public_url, object_name)
