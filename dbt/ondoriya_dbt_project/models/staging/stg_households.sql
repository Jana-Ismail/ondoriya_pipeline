{{ config(
    materialized='view',
    schema='silver'
) }}

SELECT
    household_id,
    region_id,
    household_type,
    SOURCE_FILE as _source_file,
    current_timestamp as _ingestion_timestamp_utc
FROM bronze.raw_households