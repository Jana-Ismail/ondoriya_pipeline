import duckdb
import pandas as pd
from minio.error import S3Error
from io import BytesIO

from utils.logging_utils import setup_logger
from utils.date_utils import get_current_utc_timestamp
from utils.file_utils import ensure_directory_exists
from utils.cloud_storage_utils import connect_to_minio
from config.settings import (
    LOG_FILE_PATH,
    DATA_DIR,
    DB_NAME,
    MINIO_BUCKET_NAME,
    BRONZE_SCHEMA
)

logger = setup_logger(__name__, LOG_FILE_PATH)

def main():
    ensure_directory_exists(DATA_DIR)

    conn = duckdb.connect(database=f'{DATA_DIR}/{DB_NAME}')
    conn.execute("INSTALL 'ducklake'")
    conn.execute("LOAD 'ducklake'")
    conn.execute(f"CREATE SCHEMA IF NOT EXISTS {BRONZE_SCHEMA}")

    minio_client = connect_to_minio()

    ondoriya_objects_to_process = minio_client.list_objects(
        bucket_name=MINIO_BUCKET_NAME,
        prefix='ondoriya',
        recursive=True
    )

    for obj in ondoriya_objects_to_process:
        minio_response = minio_client.get_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=obj.object_name
        )

        csv_bytes = BytesIO(minio_response.read())

        minio_response.close()
        minio_response.release_conn()

        ondoriya_df = pd.read_csv(csv_bytes)

        # add metadata
        ondoriya_df['SOURCE_FILE'] = obj.object_name
        ondoriya_df['INGESTION_TIMESTAMP_UTC'] = get_current_utc_timestamp('%Y-%m-%dT%H:%M:%S')

        file_name = obj.object_name.split('/')[-1]
        table_name_base = file_name.replace('.csv', '')
        table_name = f"raw_{table_name_base}"
        conn.execute(f"CREATE TABLE IF NOT EXISTS {BRONZE_SCHEMA}.{table_name} AS SELECT * FROM 'ondoriya_df'")

    conn.close()

if __name__ == "__main__":
    main()
