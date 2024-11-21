import logging
import pandas as pd

from src.canonical_data_model import QuarterlyReportDataModel
from src.config import StatementConfig


class Collector:
    """Class that collects all the statements and applies the necessary transformation."""

    _config: StatementConfig

    def __init__(self, statement_config: StatementConfig):
        self._config = statement_config

    def get_data(self) -> pd.DataFrame:
        """Create the data for an individual statement.

        Steps are 'reading', 'validating' with an individual statement model, 'mapping'
        to the canonical data model and once again 'validating' it.

        Returns:
            pd.DataFrame: Individual statement data mapped to canonical data model.
        """
        logging.debug(f"Processing statement: {self.config.name}")
        df_raw = self._read_data()
        self._validate_raw_data(df_raw)
        df = self._map_to_canonical(df_raw)
        self._validate_canonical_data(df)
        return df

    def _read_data(self) -> pd.DataFrame:
        """Read the data for the individual statement.

        Returns:
            pd.DataFrame: Dataframe of the individual raw statement data.
        """
        df = pd.read_csv(
            self.config.full_path,
            delimiter=self.config.reading_delimiter,
            skiprows=self.config.reading_skiprows,
            thousands=self.config.reading_thousands,
            quotechar=self.config.reading_quotechar,
            decimal=self.config.reading_decimal,
            parse_dates=[
                field_name
                for field_name, field in self.config.validation_model.to_schema().columns.items()
                if str(field.dtype) == "datetime64[ns]"
            ],
            date_format=self.config.dateformat,
        )
        return df

    def _validate_raw_data(self, df_raw_unvalidated: pd.DataFrame) -> None:
        """Validate the raw data with the coresponding statement data model.

        Args:
            df_raw_unvalidated (pd.DataFrame): The unvalidated raw data for the statement.
        """
        self.config.validation_model.validate(df_raw_unvalidated)

    def _map_to_canonical(self, df_non_canonical: pd.DataFrame) -> pd.DataFrame:
        """Map the individually validated statement data to the canonical data model.

        Args:
            df_non_canonical (pd.DataFrame): Individually validated statement data.

        Returns:
            pd.DataFrame: Statement data mapped to canonical data model.
        """

        # rename columns
        df_non_canonical.rename(columns=self.config.map_column_names, inplace=True)

        # filter unused columns
        df = df_non_canonical.filter(
            items=list(QuarterlyReportDataModel.to_schema().columns.keys())
        )

        # add account name
        df["prep_Account"] = self.config.name

        # add column if not available
        if "Kontonummer" not in df.columns:
            df["Kontonummer"] = None

        return df

    def _validate_canonical_data(self, df_unvalidated: pd.DataFrame) -> None:
        """Validate the mapped statement data with the canonical data model.

        Args:
            df_unvalidated (pd.DataFrame): The statement data mapped to the canonical data model.
        """
        QuarterlyReportDataModel.validate(df_unvalidated)

    @property
    def config(self) -> StatementConfig:
        return self._config
