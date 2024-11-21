from dataclasses import dataclass
import numpy as np
from pandera.typing import DataFrame, Series
import pandera as pa
from datetime import datetime

from src.static_input import (
    CANONICAL_DATA_MODEL_CATEGORIES,
    CANONICAL_DATA_MODEL_MONTHS,
    CANONICAL_DATA_MODEL_TRANSACTION_TYPES,
    CANONICAL_DATA_MODEL_ACCOUNTS,
)


@dataclass
class QuarterlyReportDataModel(pa.DataFrameModel):
    """Definition of the canonical data model.

    This class defines the state of data that is the minimal common denominator before
    custom columns are applied.

    'Buchungstag' - date of the transaction
    'Betrag' - value of the transaction, positive if inflow
    'Verwendungszweck' - description (if available) for the transaction
    'Kontonummer' - account number (usually iban) for the originating account, usually null
    """

    Buchungstag: Series[datetime] = pa.Field()

    Betrag: Series[float] = pa.Field(
        description="Transaction amount (positive for income, negative for expenses)",
    )

    Verwendungszweck: Series[str] = pa.Field(
        description="Transaction purpose",
    )

    Kontonummer: Series[str] = pa.Field(nullable=True)


@dataclass
class QuarterlyReportDataModelOnlyCustomColumns(pa.DataFrameModel):
    """Only custom columsn.

    prep_Year - year in format 'YYYY'
    prep_Month - month in format 'MMM'
    prep_Type - 'Umbuchung', 'Einnahmen', 'Ausgaben'
    prep_Recurring - if it is a recurring flow
    prep_Category - individually defined category
    """

    prep_Month: Series[str] = pa.Field(
        description="Prepared month in short form",
    )

    prep_Year: Series[np.int32] = pa.Field(
        description="Prepared year",
    )

    prep_Type: Series[str] = pa.Field(
        description="Type of transaction: income or expense",
    )

    prep_Recurring: Series[bool] = pa.Field(
        description="Whether the transaction is recurring or not",
    )

    prep_Category: Series[str] = pa.Field(
        description="Categorized description of the transaction",
    )
    prep_Account: Series[str] = pa.Field(
        description="Account where the transaction happened",
    )

    @pa.check("prep_Month")
    def check_month_str(cls, a: Series[str]) -> Series[bool]:
        return a.isin(CANONICAL_DATA_MODEL_MONTHS)

    @pa.check("prep_Year")
    def check_year_range(cls, a: Series[str]) -> Series[bool]:
        return a.apply((lambda x: (x >= 2000) & (x <= 2100)))

    @pa.check("prep_Type")
    def check_transaction_type(cls, a: Series[str]) -> Series[bool]:
        return a.isin(CANONICAL_DATA_MODEL_TRANSACTION_TYPES)

    @pa.check("prep_Recurring")
    def check_recurring_type(cls, a: Series[str]) -> Series[bool]:
        return a.isin([True, False])

    @pa.check("prep_Category")
    def check_category(cls, a: Series[str]) -> Series[bool]:
        return a.isin(CANONICAL_DATA_MODEL_CATEGORIES)

    @pa.check("prep_Account")
    def check_account(cls, a: Series[str]) -> Series[bool]:
        return a.isin(CANONICAL_DATA_MODEL_ACCOUNTS)

    @pa.dataframe_check
    def check_prep_type_betrag(cls, df: DataFrame) -> Series[bool]:
        """
        Ensure that if prep_Type is 'Ausgabe' (expense), Betrag is negative,
        and if prep_Type is 'Einnahme' (income), Betrag is positive.
        """
        condition_expense = (df["prep_Type"] == "Ausgabe") & (df["Betrag"] < 0)
        condition_income = (df["prep_Type"] == "Einnahme") & (df["Betrag"] >= 0)
        condition_transfer = df["prep_Type"] == "Umbuchung"
        return condition_expense | condition_income | condition_transfer
