from datetime import datetime
import pandera as pa
from pandera.typing import DataFrame, Series

DKB_DATEFORMAT = "%d.%m.%y"
DKB_VALIDATION_STATUS_ENUM = ["Gebucht"]
DKB_VALIDATION_UMSATZTYP_ENUM = ["Eingang", "Ausgang"]

DKB_MAP_COLUMN_NAMES = {
    "Buchungsdatum": "Buchungstag",
    "Betrag (€)": "Betrag",
    "IBAN": "Kontonummer",
}


class DKBDataModel(pa.DataFrameModel):
    Buchungsdatum: Series[datetime] = pa.Field()
    Wertstellung: Series[datetime] = pa.Field()
    Status: Series[str] = pa.Field()
    Zahlungspflichtige: Series[str] = pa.Field(alias="Zahlungspflichtige*r")
    Zahlungsempfaenger: Series[str] = pa.Field(alias="Zahlungsempfänger*in")
    Verwendungszweck: Series[str] = pa.Field()
    Umsatztyp: Series[str] = pa.Field()
    IBAN: Series[str] = pa.Field()
    Betrag: Series[float] = pa.Field(alias="Betrag (€)")
    Glaeubiger_ID: Series[str] = pa.Field(alias="Gläubiger-ID", nullable=True)
    Mandatsreferenz: Series[str] = pa.Field(nullable=True)
    Kundenreferenz: Series[str] = pa.Field(nullable=True)

    @pa.check("Status")
    def check_status(cls, a: Series) -> Series[bool]:
        return a.isin(DKB_VALIDATION_STATUS_ENUM)

    @pa.check("Umsatztyp")
    def check_transaction_type(cls, a: Series) -> Series[bool]:
        return a.isin(DKB_VALIDATION_UMSATZTYP_ENUM)

    @pa.dataframe_check
    def check_type_and_amount(cls, df: DataFrame) -> DataFrame[bool]:
        condition_expense = (df["Umsatztyp"] == "Ausgang") & (df["Betrag (€)"] < 0)
        condition_income = (df["Umsatztyp"] == "Eingang") & (df["Betrag (€)"] >= 0)
        return condition_expense | condition_income


dkb_statement_config = {
    "name": "DKB",
    "dateformat": DKB_DATEFORMAT,
    "map_column_names": DKB_MAP_COLUMN_NAMES,
    "validation_model": DKBDataModel,
    "reading_skiprows": 4,
    "reading_delimiter": ";",
}
