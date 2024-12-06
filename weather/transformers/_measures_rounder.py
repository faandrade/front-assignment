from typing import Any

from pandas import DataFrame

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: DataFrame, *args: Any, **kwargs: Any) -> DataFrame:
    data[["humidity", "wind_speed", "temperature"]] = data[
        ["humidity", "wind_speed", "temperature"]
    ].round(2)

    return data


@test
def test_output(output: DataFrame, *args: Any) -> None:
    rounded_columns = ["humidity", "wind_speed", "temperature"]
    for column in rounded_columns:
        decimal_places = output[column].apply(
            lambda x: len(str(x).split(".")[-1]) if "." in str(x) else 0
        )
        assert (
            decimal_places.max() <= 2
        ), f"Column {column} has values with more than 2 decimals"
