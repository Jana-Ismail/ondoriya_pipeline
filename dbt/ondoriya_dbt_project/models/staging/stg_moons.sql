{{ config(
    materialized='view',
    schema='silver'
) }}

SELECT
    "Moon_ID" as moon_id,
    "Moon_Name" as moon_name,
    "Settlement_Formal" as settlement_formal,
    "Colloquial" as colloquial,
    "Staff_Size" as staff_size,
    "Specialty" as specialty,
    "Language_Origin" as language_origin,
    SOURCE_FILE as _source_file,
    current_timestamp as _ingestion_timestamp_utc
FROM bronze.raw_moons