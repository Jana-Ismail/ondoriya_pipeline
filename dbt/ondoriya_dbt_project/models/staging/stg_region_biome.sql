{{ config(
    materialized='view',
    schema='silver'
) }}

SELECT
    "Region_ID" as region_id,
    "Full_Name" as full_name,
    "Biome" as biome,
    SOURCE_FILE as _source_file,
    current_timestamp as _ingestion_timestamp_utc
FROM bronze.raw_region_biome