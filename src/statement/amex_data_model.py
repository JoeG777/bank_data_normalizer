from pandera.typing import Series
import pandera as pa

from datetime import datetime

AMEX_DATEFORMAT = "%d/%m/%Y"
AMEX_MAP_COLUMN_NAMES = {
    "Datum": "Buchungstag",
    "Beschreibung": "Verwendungszweck",
}


class AMEXDataModel(pa.DataFrameModel):
    Datum: Series[datetime] = pa.Field()
    Beschreibung: Series[str] = pa.Field()
    Karteninhaber: Series[str] = pa.Field()
    Konto: Series[int] = pa.Field(
        alias="Konto #"
    )  # NOTE: not really int but could infered as such, discarded so not important
    Betrag: Series[float] = pa.Field()


amex_statement_config = {
    "name": "AMEX",
    "dateformat": AMEX_DATEFORMAT,
    "map_column_names": AMEX_MAP_COLUMN_NAMES,
    "validation_model": AMEXDataModel,
}
