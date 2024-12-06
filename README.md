# Weather Data Pipeline

## Prerequisites
- Docker installed on your system

## Setup
1. Copy the environment variables file:

```bash
cp .env.dev .env
```

2. Start the containers:



```bash
docker compose up
```


## Access Points
- **Mage UI**: `http://localhost:6789`
- **PostgreSQL Database**: 
  - Host: `localhost`
  - Port: `5432`

## Runtime Variables
The pipeline accepts two parameters:

1. `station_id` (default: "0128W")
   - Weather station identifier

2. `reference_date` (optional)
   - Format: "yyyy-mm-dd"
   - If not provided, defaults to execution date
   - Pipeline will fetch data from reference date back to 7 days prior
  
## Pipeline Execution Guide

1. Navigate to `http://localhost:6789/pipelines`
2. Click on the pipeline name (e.g., "weather_data")
3. Click the "Run@Once" button to create a new trigger
4. In the trigger configuration, you can set:
   - `station_id`: Weather station identifier
   - `reference_date`: Target date in "yyyy-mm-dd" format



