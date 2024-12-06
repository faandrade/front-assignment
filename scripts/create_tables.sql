CREATE TABLE stations (

    id SERIAL PRIMARY KEY,
    external_id TEXT,
    name TEXT,
    timezone TEXT,
    lat NUMERIC,
    long NUMERIC
);

CREATE TABLE weather_facts (
    dim_station_id INTEGER,
    obs_timestamp TEXT,
    m_temperature NUMERIC,
    m_wind_speed NUMERIC,
    m_humidity NUMERIC,
    PRIMARY KEY (dim_station_id, obs_timestamp),
    FOREIGN KEY (dim_station_id) REFERENCES stations(id)

);


CREATE TABLE intermediate_weather_facts (
    dim_station_id INTEGER,
    obs_timestamp TEXT,
    m_temperature NUMERIC,
    m_wind_speed NUMERIC,
    m_humidity NUMERIC
);