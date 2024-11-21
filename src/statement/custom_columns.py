import numpy as np
import pandas as pd

from src.personal_information import (
    MY_CATEGORIES_IBAN,
    MY_CATEGORY_BESCHREIBUNG,
    MY_IBANS,
    MY_RECURRING_EXPENSES_IBAN,
    MY_RECURRING_INCOME_IBAN,
)


def create_custom_columns(df: pd.DataFrame) -> pd.DataFrame:
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
                df["Verwendungszweck"].str.lower().str.contains(text), "prep_Category"
            ] = category

    df.loc[df["prep_Type"] == "Umbuchung", "prep_Category"] = "Umbuchung"

    return df
