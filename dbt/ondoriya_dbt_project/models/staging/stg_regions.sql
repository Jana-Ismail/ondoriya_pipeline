{{ config(
    materialized='view',
    schema='silver'
) }}

SELECT
    "Region_ID" as region_id,
    "Ancient_Name" as ancient_name,
    "Current_Faction" as current_faction,
    "Era_Tag" as era_tag,
    "Full_Name" as full_name,
    "Colloquial_Name" as colloquial_name,
    "Founding_Era" as founding_era,
    "Density_Tier" as density_tier,
    "Capital" as capital,
    "Primary_Industry" as primary_industry,
    "Founding_Story" as founding_story,
    "Vote_History_Last3" as vote_history_last3,
    "Key_Pressure_Points" as key_pressure_points,
    "Unbound_Presence" as unbound_presence,
    SOURCE_FILE as _source_file,
    current_timestamp as _ingestion_timestamp_utc
FROM bronze.raw_regions