{{ config(materialized='table', schema='gold') }}

WITH region_population AS (
    SELECT
        p.current_region_id as region_id,
        COUNT(*) as population_count,
        COUNT(DISTINCT p.household_id) as household_count
    FROM {{ ref('stg_people') }} p
    GROUP BY p.current_region_id
),

household_analysis AS (
    SELECT
        h.region_id,
        COUNT(*) as total_households,
        COUNT(CASE WHEN h.household_type = 'ruling' THEN 1 END) as ruling_households,
        COUNT(CASE WHEN h.household_type != 'ruling' THEN 1 END) as non_ruling_households
    FROM {{ ref('stg_households') }} h
    GROUP BY h.region_id
)

SELECT
    r.region_id,
    r.ancient_name,
    r.full_name as region_name,
    r.colloquial_name,
    r.current_faction,
    r.density_tier,
    r.capital,
    r.primary_industry,
    
    -- Population metrics
    COALESCE(rp.population_count, 0) as population_count,
    COALESCE(rp.household_count, 0) as household_count,
    
    -- Household analysis 
    COALESCE(ha.total_households, 0) as total_households,
    COALESCE(ha.ruling_households, 0) as ruling_households,
    COALESCE(ha.non_ruling_households, 0) as non_ruling_households,
    
    -- Population density calculations
    CASE 
        WHEN r.density_tier = 'Dense' THEN 4
        WHEN r.density_tier = 'Settled' THEN 3
        WHEN r.density_tier = 'Sparse' THEN 2
        WHEN r.density_tier = 'Wastes' THEN 1
        ELSE 0
    END as density_score,
    
    -- Population per household
    CASE 
        WHEN COALESCE(rp.household_count, 0) > 0 
        THEN ROUND(COALESCE(rp.population_count, 0) * 1.0 / rp.household_count, 1)
        ELSE 0 
    END as avg_people_per_household,
    
    -- Population ranking
    ROW_NUMBER() OVER (ORDER BY COALESCE(rp.population_count, 0) DESC) as population_rank,
    
    -- Percentage of total population
    ROUND(
        100.0 * COALESCE(rp.population_count, 0) / 
        SUM(COALESCE(rp.population_count, 0)) OVER(), 
        2
    ) as percentage_of_total_population

FROM {{ ref('stg_regions') }} r
LEFT JOIN region_population rp ON r.region_id = rp.region_id
LEFT JOIN household_analysis ha ON r.region_id = ha.region_id

ORDER BY population_count DESC, r.region_id