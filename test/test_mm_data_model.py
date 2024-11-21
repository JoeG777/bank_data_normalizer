from pathlib import Path
import pandas as pd
import pytest

from src.canonical_data_model import QuarterlyReportDataModel
from src.statement.mm_data_model import MMDataModel, map_mm_to_canonical


@pytest.fixture
def read_mm_data_model_fixture() -> pd.DataFrame:
    df = pd.read_csv(
        Path("test/test_data/2024Q3 - MM.csv"),
        delimiter=",",
        skiprows=4,
        thousands=".",
        quotechar='"',
        decimal=",",
        parse_dates=["Belegdatum", "Wertstellung"],
        date_format="%d.%m.%y",
    )
    return df


def test_dkb_data_model(read_mm_data_model_fixture: pd.DataFrame) -> None:
    MMDataModel.validate(read_mm_data_model_fixture)


def test_map_mm(read_mm_data_model_fixture: pd.DataFrame) -> None:
    df_test = read_mm_data_model_fixture.copy()
    MMDataModel.validate(df_test)
    result = map_mm_to_canonical(df_test)
    QuarterlyReportDataModel.validate(result)
