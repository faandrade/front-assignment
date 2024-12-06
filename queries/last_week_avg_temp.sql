WITH facts_in_utc AS (
SELECT
	wf.*,
	wf.obs_timestamp::TIMESTAMP AT TIME ZONE s.timezone AT TIME ZONE 'UTC' AS utc_obs_timestamp
FROM
	weather_facts wf
JOIN stations s ON
	wf.dim_station_id = s.id 
),
last_week_facts AS (
SELECT
	*
FROM
	facts_in_utc
WHERE
	(utc_obs_timestamp >= date_trunc('week',
	NOW() AT TIME ZONE 'UTC' - INTERVAL '1 week')
		AND
       utc_obs_timestamp < date_trunc('week',
		NOW() AT TIME ZONE 'UTC')
      ) 
)

SELECT dim_station_id, AVG(m_temperature) AS last_week_avg_temp 
FROM last_week_facts
GROUP BY dim_station_id