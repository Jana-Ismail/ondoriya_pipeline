{{ config(
    materialized='view',
    schema='silver'
) }}

SELECT
    "Faction" as faction_name,
    "Regions" as regions,
    "Percent" as percent,
    "SOURCE_FILE" as _source_file,
    current_timestamp as _ingestion_timestamp_utc
FROM bronze.raw_faction_distribution