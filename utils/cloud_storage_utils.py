from minio import Minio

from config.settings import MINIO_ACCESS_KEY, MINIO_URL_HOST_PORT, MINIO_SECRET_KEY

def connect_to_minio():
    minio_client = Minio(
        endpoint=MINIO_URL_HOST_PORT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )

    return minio_client
