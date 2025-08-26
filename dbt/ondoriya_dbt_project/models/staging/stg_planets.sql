{{ config(
    materialized='view',
    schema='silver'
) }}

SELECT
    "World_ID" as world_id,
    "World_Name" as world_name,
    "Star_System" as star_system,
    "Planet_Type" as planet_type,
    "Gravity_g" as gravity_g,
    "Day_Length_hours" as day_length_hours,
    "Year_Length_days" as year_length_days,
    "Axial_Tilt_deg" as axial_tilt_deg,
    "Calendar_Name" as calendar_name,
    SOURCE_FILE as _source_file,
    current_timestamp as _ingestion_timestamp_utc
FROM bronze.raw_planets