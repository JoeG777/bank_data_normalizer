import pandera as pa
from datetime import datetime
from pandera.typing import Series, DataFrame


MM_VALIDATION_STATUS_ENUM = ["Gebucht"]
MM_VALIDATION_UMSATZTYP_ENUM = [
    "Entgelt",
    "Im Geschäft",
    "Lastschrift",
    "Bargeldabhebung",
    "Onlinezahlung",
]

MM_DATEFORMAT = "%d.%m.%y"
MM_MAP_COLUMN_NAMES = {
    "Belegdatum": "Buchungstag",
    "Betrag (€)": "Betrag",
    "Beschreibung": "Verwendungszweck",
}


class MMDataModel(pa.DataFrameModel):
    Belegdatum: Series[datetime] = pa.Field()
    Wertstellung: Series[datetime] = pa.Field()
    Status: Series[str] = pa.Field()
    Beschreibung: Series[str] = pa.Field()
    Umsatztyp: Series[str] = pa.Field()
    Betrag: Series[float] = pa.Field(alias="Betrag (€)")
    Fremdwährungsbetrag: Series[float] = pa.Field(nullable=True)

    @pa.check("Status")
    def check_status(cls, a: Series) -> Series[bool]:
        return a.isin(MM_VALIDATION_STATUS_ENUM)

    @pa.check("Umsatztyp")
    def check_transaction_type(cls, a: Series) -> Series[bool]:
        return a.isin(MM_VALIDATION_UMSATZTYP_ENUM)

    @pa.dataframe_check
    def check_type_and_amount(cls, df: DataFrame) -> DataFrame[bool]:
        condition_equalizer = (df["Umsatztyp"] == "Lastschrift") & (
            df["Betrag (€)"] > 0
        )
        condition_outflow = (df["Umsatztyp"] != "Lastschrift") & (df["Betrag (€)"] < 0)
        return condition_equalizer | condition_outflow


mm_statement_config = {
    "name": "MM",
    "dateformat": MM_DATEFORMAT,
    "map_column_names": MM_MAP_COLUMN_NAMES,
    "validation_model": MMDataModel,
    "reading_skiprows": 4,
    "reading_delimiter": ";",
}
