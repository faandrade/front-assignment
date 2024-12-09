from datetime import datetime, timedelta
from typing import Any

import pandas as pd
import requests

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(
    station_df: pd.DataFrame, *args: Any, **kwargs: Any
) -> pd.DataFrame:
    url = f"https://api.weather.gov/stations/{kwargs['station_id']}/observations"

    if kwargs["reference_date"]:
        reference_date = datetime.strptime(
            kwargs["reference_date"], "%Y-%m-%d"
        ).replace(hour=23, minute=59, second=59, microsecond=999999)

    else:
        reference_date = kwargs["execution_date"].replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

    start_date = (reference_date - timedelta(days=7)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    start_date_str = pd.Timestamp(start_date).isoformat() + "Z"
    reference_date_str = pd.Timestamp(reference_date).isoformat() + "Z"

    print(
        f"Getting Observation data for station {kwargs['station_id']}, from {start_date_str} to {reference_date_str}"
    )

    params = {
        "start": start_date_str,
        "end": reference_date_str,
    }

    headers = {"accept": "application/geo+json"}

    response = requests.get(url, params=params, headers=headers).json()

    if "features" not in response.keys():
        raise KeyError("Error accessing observations data")

    obs_timestamps = []
    temperatures = []
    wind_speeds = []
    humidities = []

    for record in response.get("features", []):
        obs_timestamps.append(record.get("properties", {}).get("timestamp"))
        temperatures.append(
            record.get("properties", {}).get("temperature", {}).get("value")
        )
        wind_speeds.append(
            record.get("properties", {}).get("windSpeed", {}).get("value")
        )
        humidities.append(
            record.get("properties", {}).get("relativeHumidity", {}).get("value")
        )

    df = pd.DataFrame(
        {
            "obs_timestamp": obs_timestamps,
            "temperature": temperatures,
            "wind_speed": wind_speeds,
            "humidity": humidities,
        }
    )

    df = df.assign(id=station_df["id"].iloc[0])

    return df


@test
def test_output(output: pd.DataFrame, *args: Any) -> None:
    output = output[[col for col in output.columns if col != "id"]]
    assert not output.empty, "Observations DataFrame is empty"


@test
def test_output_schema(output: pd.DataFrame, *args: Any) -> None:
    required_columns = ["id", "obs_timestamp", "temperature", "wind_speed", "humidity"]
    assert all(
        col in output.columns for col in required_columns
    ), "Missing columns in DataFrame"


@test
def test_output_valid_rows(output: pd.DataFrame, *args: Any) -> None:
    non_nullable_columns = ["temperature", "wind_speed", "humidity"]
    assert (
        output[non_nullable_columns].isnull().sum().sum()
        != len(non_nullable_columns) * output.shape[1]
    ), "The DataFrame only have NULL values"
