import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent

LOG_DIR = PROJECT_ROOT / 'logs'
LOG_FILE_NAME = 'ondoriya_data_pipeline.log'
LOG_FILE_PATH = LOG_DIR / LOG_FILE_NAME

API_BASE_URL = 'https://sample.ondoriya.com'

DATA_DIR = PROJECT_ROOT / 'datalake'
DB_NAME = 'ondoriya.duckdb'
DB_PATH = DATA_DIR / DB_NAME

BRONZE_SCHEMA = 'bronze'
SILVER_SCHEMA = 'silver'
GOLD_SCHEMA = 'gold'

METABASE_DB_NAME = 'metabase_data.db'

FILES_TO_INGEST = [
    "faction_distribution.csv",
    "households.csv",
    "language_building_blocks.csv",
    "language_roots.csv",
    "moons.csv",
    "people.csv",
    "planets.csv",
    "region_biome.csv",
    "regions.csv"
]

MINIO_BUCKET_NAME=os.getenv('MINIO_BUCKET_NAME')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_URL_HOST_PORT = os.getenv('MINIO_URL_HOST_PORT')