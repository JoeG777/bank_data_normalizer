from pathlib import Path
from src.canonical_data_model import QuarterlyReportDataModelOnlyCustomColumns
import pandas as pd
import pytest
from datetime import datetime

from src.static_input import CANONICAL_DATA_MODEL_DATEFORMAT


@pytest.fixture
def read_canonical_data_model_fixture() -> pd.DataFrame:
    df = pd.read_csv(
        Path("test/test_data/test_data.csv"),
        delimiter=";",
        thousands=",",
        decimal=".",
        parse_dates=[
            field_name
            for field_name, field in QuarterlyReportDataModelOnlyCustomColumns.to_schema().columns.items()
            if str(field.dtype) == "datetime64[ns]"
        ],
        date_format=CANONICAL_DATA_MODEL_DATEFORMAT,
    )
    return df


@pytest.fixture
def canonical_data_model_fixture() -> pd.DataFrame:
    data = {
        "Buchungstag": [
            datetime(2023, 1, 15),
            datetime(2023, 1, 16),
            datetime(2023, 2, 15),
        ],
        "Betrag": [
            300.00,
            400.00,
            -30.00,
        ],
        "Verwendungszweck": ["Salary Payment", "Freelance Project", "Grocery Shopping"],
        "prep_Month": ["Jan", "Jan", "Jan"],
        "prep_Year": [2023, 2023, 2023],
        "prep_Type": [
            "Einnahme",
            "Einnahme",
            "Ausgabe",
        ],
        "prep_Recurring": [True, False, True],
        "prep_Category": ["Lohn/Gehalt", "Wohnen", "Essen"],
        "prep_Account": ["CASH", "PP", "MM"],
    }
    df = pd.DataFrame(data)
    return df


def test_canonical_data_model(read_conoical_data_model_fixture: pd.DataFrame) -> None:
    QuarterlyReportDataModelOnlyCustomColumns.validate(read_conoical_data_model_fixture)
