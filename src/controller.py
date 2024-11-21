import numpy as np
import pandas as pd

from src.canonical_data_model import (
    QuarterlyReportDataModelOnlyCustomColumns,
    QuarterlyReportDataModel,
)
from src.config import QUARTERLY_REPORT_EXPORT_FILENAME, QUARTERLY_REPORT_STATEMENTS_DIR
from src.personal_information import (
    MY_CATEGORIES_IBAN,
    MY_CATEGORY_BESCHREIBUNG,
    MY_IBANS,
    MY_RECURRING_EXPENSES_IBAN,
    MY_RECURRING_INCOME_IBAN,
)
from src.collector import Collector
from src.config import StatementConfig


class Controller:
    """The 'Controller' class controls the main steps to process the data."""

    def process_statements(statements: list[StatementConfig]) -> pd.DataFrame:
        """

        1. Read in the configuration for the individual statements
        2. Get the canonical data from each statement
        3. Concatenate the canonical data to one big dataframe
        4. Validate the canonical data (without the custom columns)
        Args:
            statements (list[StatementConfig]): List of statement configurations.

        Returns:
            pd.DataFrame: A canonical dataframe without custom columns
        """
        collectors = [Collector(statement) for statement in statements]
        df = pd.concat(
            [collector.get_data() for collector in collectors], ignore_index=True
        )
        QuarterlyReportDataModel.validate(df)
        return df

    def validate_canonical_data_model(df: pd.DataFrame) -> None:
        """Validate data with the canonical data model."""
        QuarterlyReportDataModel.validate(df)
        QuarterlyReportDataModelOnlyCustomColumns.validate(df)

    def add_custom_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Add custom columns to the canonical dataframe.

        prep_Year - year in format 'YYYY'
        prep_Month - month in format 'MMM'
        prep_Type - 'Umbuchung', 'Einnahmen', 'Ausgaben'
        prep_Recurring - if it is a recurring flow
        prep_Category - individually defined category

        Args:
            df (pd.DataFrame): canonical dataframe

        Returns:
            pd.DataFrame: canonical dataframe with custom models
        """
        QuarterlyReportDataModel.validate(df)
        df["prep_Year"] = df["Buchungstag"].dt.year
        df["prep_Month"] = df["Buchungstag"].dt.strftime("%b")

        # create transfer type ("prep_Type")
        df["prep_Type"] = np.where(df["Betrag"] >= 0, "Einnahme", "Ausgabe")

        for iban in MY_IBANS.values():
            df.loc[df["Kontonummer"] == iban, "prep_Type"] = "Umbuchung"

        # create recurring
        df["prep_Recurring"] = False

        for iban in list(MY_RECURRING_EXPENSES_IBAN.values()) + list(
            MY_RECURRING_INCOME_IBAN.values()
        ):
            df.loc[
                df["Kontonummer"] == iban,
                "prep_Recurring",
            ] = True

        # create categories
        df["prep_Category"] = "NOT ASSIGNED"
        for category, ibans in MY_CATEGORIES_IBAN.items():
            for iban in ibans:
                df.loc[df["Kontonummer"] == iban, "prep_Category"] = category

        for category, texts in MY_CATEGORY_BESCHREIBUNG.items():
            for text in texts:
                df.loc[
                    df["Verwendungszweck"].str.lower().str.contains(text),
                    "prep_Category",
                ] = category

        df.loc[df["prep_Type"] == "Umbuchung", "prep_Category"] = "Umbuchung"

        return df

    def export_data(df: pd.DataFrame) -> None:
        """Export the dataframe to csv.

        Path is determined by given directory and filename.

        Args:
            df (pd.DataFrame): dataframe to export
        """
        df.to_csv(
            QUARTERLY_REPORT_STATEMENTS_DIR / QUARTERLY_REPORT_EXPORT_FILENAME,
            sep=";",
            header=True,
        )
