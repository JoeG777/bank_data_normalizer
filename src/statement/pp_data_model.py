import pandera as pa
from pandera.typing import Series

from datetime import datetime

PP_DATEFORMAT = "%d.%m.%Y"

PP_MAP_COLUMN_NAMES = {
    "Datum": "Buchungstag",
    "Beschreibung": "Verwendungszweck",
    "Brutto": "Betrag",
}


class PPDataModel(pa.DataFrameModel):
    Datum: Series[datetime] = pa.Field()
    Uhrzeit: Series[str] = pa.Field()
    Zeitzone: Series[str] = pa.Field()
    Beschreibung: Series[str] = pa.Field()
    Währung: Series[str] = pa.Field()
    Brutto: Series[float] = pa.Field()
    Entgelt: Series[float] = pa.Field()
    Netto: Series[float] = pa.Field()
    Guthaben: Series[float] = pa.Field()
    Transaktionscode: Series[str] = pa.Field()
    Absender: Series[str] = pa.Field(alias="Absender E-Mail-Adresse", nullable=True)
    Name: Series[str] = pa.Field(nullable=True)
    Bank: Series[str] = pa.Field(alias="Name der Bank", nullable=True)
    Bankkonto: Series[str] = pa.Field(nullable=True)
    Versand: Series[float] = pa.Field(alias="Versand- und Bearbeitungsgebühr")
    Umsatzsteuer: Series[float] = pa.Field()
    Rechnungsnummer: Series[str] = pa.Field(nullable=True)
    zugehörig: Series[str] = pa.Field(
        alias="Zugehöriger Transaktionscode", nullable=True
    )


pp_statement_config = {
    "name": "PP",
    "dateformat": PP_DATEFORMAT,
    "map_column_names": PP_MAP_COLUMN_NAMES,
    "validation_model": PPDataModel,
}
