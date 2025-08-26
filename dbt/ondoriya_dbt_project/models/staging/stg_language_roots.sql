{{ config(
    materialized='view',
    schema='silver'
) }}

SELECT
    "Root" as root,
    "Meaning" as meaning,
    "Notes" as notes,
    SOURCE_FILE as _source_file,
    current_timestamp as _ingestion_timestamp_utc
FROM bronze.raw_language_roots