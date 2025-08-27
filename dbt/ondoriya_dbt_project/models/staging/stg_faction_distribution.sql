{{ config(
    materialized='view',
    schema='silver'
) }}

SELECT
    "Faction" AS faction_name,
    "Regions" AS region_count,
    CAST(REPLACE("Percent", '%', '') AS FLOAT) as percent_numeric,
    ROW_NUMBER() OVER (ORDER BY percent_numeric DESC) AS faction_rank,
    "SOURCE_FILE" as _source_file,
    current_timestamp as _ingestion_timestamp_utc
FROM bronze.raw_faction_distribution