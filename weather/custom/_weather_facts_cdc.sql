-- Docs: https://docs.mage.ai/guides/sql-blocks
--INSERT INTO postgres.public.intermediate_weather_facts
SELECT iwf.*
FROM intermediate_weather_facts iwf 
LEFT JOIN weather_facts wf 
ON iwf.dim_station_id = wf.dim_station_id 
AND iwf.obs_timestamp = wf.obs_timestamp
WHERE wf.dim_station_id is NULL