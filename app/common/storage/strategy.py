import logging
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import boto3
import requests
from botocore.exceptions import ClientError

from app.common.storage.abstract import ImageStorage
from app.core.config import get_settings


class S3ImageStorage(ImageStorage):
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=get_settings().AWS_ACCESS_KEY_ID,
            aws_secret_access_key=get_settings().AWS_SECRET_ACCESS_KEY,
            endpoint_url=get_settings().AWS_ENDPOINT_URL,
        )
        self.bucket = get_settings().AWS_BUCKET_NAME
        self.ensure_bucket_exists()

    def ensure_bucket_exists(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket)
        except ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                self.s3.create_bucket(Bucket=self.bucket)
            else:
                raise

    def upload_image(self, image_url: str) -> Optional[str]:
        try:
            filename = Path(urlparse(image_url).path).name
            if not filename:
                filename = f"image_{hash(image_url)}"

            response = requests.get(image_url)
            response.raise_for_status()
            image_data = response.content

            key = f"images/{filename}"
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=image_data,
                ContentType=response.headers.get("Content-Type", "image/jpeg"),
            )

            return f"{get_settings().AWS_ENDPOINT_URL}/{self.bucket}/{key}"
        except Exception as e:
            logging.error("Error uploading image: %s", e)
            return None
