from __future__ import annotations

from functools import lru_cache
from io import BytesIO

from minio import Minio
from .config import Settings, settings


class MinioObjectStorage:
    def __init__(self, client: Minio, bucket: str) -> None:
        self._client = client
        self._bucket = bucket

    @classmethod
    def make_storage(cls, app_settings: Settings) -> MinioObjectStorage:
        endpoint = _require(app_settings.minio_endpoint, "MINIO_ENDPOINT")
        access_key = _require(app_settings.minio_access_key, "MINIO_ACCESS_KEY")
        secret_key = _require(app_settings.minio_secret_key, "MINIO_SECRET_KEY")
        bucket = _require(app_settings.minio_bucket, "MINIO_BUCKET")

        client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=app_settings.minio_secure
        )
        return cls(client=client, bucket=bucket)

    def put_pdf(self, object_name: str, content: bytes) -> None:
        self._client.put_object(
            bucket_name=self._bucket,
            object_name=object_name,
            data=BytesIO(content),
            length=len(content),
            content_type="application/pdf",
        )


def _require(value: str | None, env_name: str) -> str:
    if not value:
        raise RuntimeError(f"Missing required setting: {env_name}")
    return value

@lru_cache
def get_minio_object_storage() -> MinioObjectStorage:
    return MinioObjectStorage.make_storage(settings)
