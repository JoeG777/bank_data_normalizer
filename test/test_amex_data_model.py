from pathlib import Path
import pandas as pd
import pytest

from src.canonical_data_model import QuarterlyReportDataModel
from src.statement.amex_data_model import AMEXDataModel, map_amex_to_canonical


@pytest.fixture
def read_amex_data_model_fixture() -> pd.DataFrame:
    df = pd.read_csv(
        Path("test/test_data/2024Q3 - AMEX.csv"),
        delimiter=",",
        thousands=".",
        quotechar='"',
        decimal=",",
        parse_dates=["Datum"],
        date_format="%d/%m/%Y",
    )
    return df


def test_mm_data_model(read_amex_data_model_fixture: pd.DataFrame) -> None:
    AMEXDataModel.validate(read_amex_data_model_fixture)


def test_map_amex(read_amex_data_model_fixture: pd.DataFrame) -> None:
    df_test = read_amex_data_model_fixture.copy()
    AMEXDataModel.validate(df_test)
    result = map_amex_to_canonical(df_test)
    QuarterlyReportDataModel.validate(result)
