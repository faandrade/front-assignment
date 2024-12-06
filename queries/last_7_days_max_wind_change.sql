WITH last_seven_days_facts AS (
SELECT
	wf.*
FROM
	weather_facts wf
JOIN stations s ON
	wf.dim_station_id = s.id
WHERE
	wf.obs_timestamp::TIMESTAMP AT TIME ZONE s.timezone AT TIME ZONE 'UTC' >= date_trunc('day',
	NOW() AT TIME ZONE 'UTC' - INTERVAL '1 week')
	-- this filters last 7 days of records  
)
,
last_wind AS (
SELECT
	dim_station_id,
	obs_timestamp,
	m_wind_speed,
	LAG(m_wind_speed) OVER (PARTITION BY dim_station_id
ORDER BY
	obs_timestamp) AS last_wind_measure
FROM
	last_seven_days_facts wf
)	
,
wind_changes AS (
SELECT
	last_wind.*,
	ABS(m_wind_speed - CASE
		WHEN last_wind_measure IS NULL THEN m_wind_speed
		ELSE last_wind_measure
	END) AS wind_change
FROM
	last_wind
	)
	

SELECT
	dim_station_id,
	max(wind_change) AS max_wind_change
FROM
	wind_changes
GROUP BY
	dim_station_id