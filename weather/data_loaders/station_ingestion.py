from typing import Any

import pandas as pd
import requests

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args: Any, **kwargs: Any) -> pd.DataFrame:
    url = f'https://api.weather.gov/stations/{kwargs["station_id"]}'
    response = requests.get(url).json()

    return pd.DataFrame(
        {
            "external_id": [kwargs.get("station_id")],
            "name": [response.get("properties", {}).get("name")],
            "timezone": [response.get("properties", {}).get("timeZone")],
            "lat": [response.get("geometry", {}).get("coordinates", [None, None])[0]],
            "long": [response.get("geometry", {}).get("coordinates", [None, None])[1]],
        }
    )


@test
def test_output(output: pd.DataFrame, *args: any) -> None:
    assert isinstance(output, pd.DataFrame), "Output must be a pandas DataFrame"

    for column in output.columns:
        assert not output[column].isnull().any(), f"Column {column} has NULL values"

    assert len(output) == 1, "Output must contain data for 1 Station"
