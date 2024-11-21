from pathlib import Path
import pandas as pd
import pytest

from src.canonical_data_model import QuarterlyReportDataModel
from src.statement.pp_data_model import PPDataModel, map_pp_to_canonical


@pytest.fixture
def read_pp_data_model_fixture() -> pd.DataFrame:
    df = pd.read_csv(
        Path("test/test_data/2024Q3 - PP.csv"),
        delimiter=",",
        thousands=".",
        quotechar='"',
        decimal=",",
        parse_dates=["Datum"],
        date_format="%d.%m.%Y",
    )
    return df


def test_mm_data_model(read_pp_data_model_fixture: pd.DataFrame) -> None:
    PPDataModel.validate(read_pp_data_model_fixture)


def test_map_pp(read_pp_data_model_fixture: pd.DataFrame) -> None:
    df_test = read_pp_data_model_fixture.copy()
    PPDataModel.validate(df_test)
    result = map_pp_to_canonical(df_test)
    QuarterlyReportDataModel.validate(result)
