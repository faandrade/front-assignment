-- Docs: https://docs.mage.ai/guides/sql-blocks
SELECT
	df.id AS dim_station_id,
	df.obs_timestamp as obs_timestamp,
	df.temperature AS m_temperature,
	df.wind_speed AS m_wind_speed,
	df.humidity AS m_humidity
    
FROM
	{{df_1}} as df