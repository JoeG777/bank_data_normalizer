from pathlib import Path
import pandas as pd
import pytest

from src.canonical_data_model import QuarterlyReportDataModel
from src.statement.dkb_data_model import DKBDataModel, map_dkb_to_canonical


@pytest.fixture
def read_dkb_data_model_fixture() -> pd.DataFrame:
    df = pd.read_csv(
        Path("test/test_data/2024Q3 - DKB.csv"),
        delimiter=",",
        skiprows=4,
        thousands=".",
        quotechar='"',
        decimal=",",
        parse_dates=["Buchungsdatum", "Wertstellung"],
        date_format="%d.%m.%y",
    )
    return df


def test_dkb_data_model(read_dkb_data_model_fixture: pd.DataFrame) -> None:
    DKBDataModel.validate(read_dkb_data_model_fixture)


def test_map_dkb(read_dkb_data_model_fixture: pd.DataFrame) -> None:
    df_test = read_dkb_data_model_fixture.copy()
    DKBDataModel.validate(df_test)
    result = map_dkb_to_canonical(df_test)
    QuarterlyReportDataModel.validate(result)
