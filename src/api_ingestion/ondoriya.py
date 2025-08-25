import os
import pandas as pd
import requests
from io import BytesIO
from minio import Minio
from minio.error import S3Error

from utils.logging_utils import setup_logger
from utils.date_utils import get_current_utc_iso_timestamp
from config.settings import (
    API_BASE_URL, 
    LOG_FILE_PATH,
    MINIO_BUCKET_NAME,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_URL_HOST_PORT,
    FILES_TO_INGEST
)

logger = setup_logger(__name__, log_file=LOG_FILE_PATH)

minio_client = Minio(
    endpoint=MINIO_URL_HOST_PORT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def get_csv_data_from_api(file_name, file_url):
    logger.info(f'Fetching data from file: {file_name} at url: {file_url}')
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        logger.info(f'Successfully fetched CSV data from file {file_name} at url {file_url}')
    except requests.RequestException as e:
        logger.error(f'Error downloading CSV data from file {file_name} at url {file_url}')
    
    content = response.content if response else None

    return content

def upload_csv_to_minio(bytes_data, file_url, timestamp):
    file_name = os.path.basename(file_url)
    object_name = f'ondoriya/{file_name}_{timestamp}.csv'
    try:
        minio_client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=object_name,
            data=BytesIO(bytes_data),
            length=len(bytes_data),
            content_type='text/csv'
        )
        logger.info(f'Successfully uploaded CSV file {file_name} to MinIO at {object_name}')
    except S3Error as e:
        logger.error(f'Error uploading CSV data to MinIO: {e}')

def main():
    for file_name in FILES_TO_INGEST:
        file_url = f'{API_BASE_URL}/{file_name}'
        csv_data = get_csv_data_from_api(file_name, file_url)
        if csv_data:
            timestamp = get_current_utc_iso_timestamp()
            upload_csv_to_minio(csv_data, file_url, timestamp)

if __name__ == "__main__":
    main()
