from typing import Any

from pandas import DataFrame

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df: DataFrame, *args: Any, **kwargs: Any) -> DataFrame:
    return df.dropna()


@test
def test_output_null_values(output: DataFrame, *args: Any) -> None:
    assert output.isnull().sum().sum() == 0, "Clean DataFrame contains NULL values"
