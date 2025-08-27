import requests
from io import BytesIO
from minio.error import S3Error

from utils.logging_utils import setup_logger
from utils.cloud_storage_utils import connect_to_minio
from config.settings import (
    API_BASE_URL,
    LOG_FILE_PATH,
    MINIO_BUCKET_NAME,
    FILES_TO_INGEST
)

logger = setup_logger(__name__, log_file=LOG_FILE_PATH)

minio_client = connect_to_minio()

def get_csv_data_from_api(file_name, file_url):
    logger.info(f'Fetching data from file: {file_name} at url: {file_url}')
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        logger.info(f'Successfully fetched CSV data from file {file_name} at url {file_url}')
    except requests.RequestException as e:
        logger.error(f'Error downloading CSV data from file {file_name} at url {file_url}: {e}')
    
    content = response.content if response else None

    return content

def upload_csv_to_minio(bytes_data, base_file_name):
    logger.info(f'Uploading CSV data to MinIO from url: {API_BASE_URL}/{base_file_name}.csv')
    object_name = f'ondoriya/{base_file_name}.csv'

    try:
        minio_client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=object_name,
            data=BytesIO(bytes_data),
            length=len(bytes_data),
            content_type='text/csv'
        )
        logger.info(f'Successfully uploaded CSV file {base_file_name} to MinIO at {object_name}')

    except S3Error as e:
        logger.error(f'Error uploading CSV data to MinIO: {e}')

def main():
    # timestamp = get_current_utc_timestamp('%Y%m%d_%H%M%S')
    
    for file_name in FILES_TO_INGEST:
        base_file_name, _ = file_name.split('.')
        print(f'file_name: {base_file_name}')
        file_url = f'{API_BASE_URL}/{file_name}'
        csv_data = get_csv_data_from_api(base_file_name, file_url)
        if csv_data:
            upload_csv_to_minio(csv_data, base_file_name)

if __name__ == "__main__":
    main()
