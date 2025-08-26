{{ config(
    materialized='view',
    schema='silver'
) }}

SELECT
    "Language_ID" as language_id,
    "Language_Name" as language_name,
    "Branch_From" as branch_from,
    "Phonology_Notes" as phonology_notes,
    "Morphology_Patterns" as morphology_patterns,
    "Example_Roots" as example_roots,
    SOURCE_FILE as _source_file,
    current_timestamp as _ingestion_timestamp_utc
FROM bronze.raw_language_building_blocks