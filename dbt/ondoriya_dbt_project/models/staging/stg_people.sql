{{ config(
    materialized='view',
    schema='silver'
) }}

SELECT
    person_id,
    first_name,
    age,
    language,
    current_region_id,
    household_id,
    family_name,
    SOURCE_FILE AS _source_file,
    current_timestamp AS _ingestion_timestamp_utc
FROM bronze.raw_people