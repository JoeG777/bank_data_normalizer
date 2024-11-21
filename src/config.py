from dataclasses import dataclass, field
from datetime import date
import os
from pathlib import Path
import pandera as pa
from dotenv import load_dotenv

load_dotenv(".env")

# master data
QUARTERLY_REPORT_ROOT_DIR: Path = Path(os.environ["QUARTERLY_REPORT_ROOT_DIR_STR"])
QUARTERLY_REPORT_BASE_FILENAME = "Quarterly Report"
QUARTERLY_REPORT_FILE_EXTENSION = "csv"

# changes each execution
QUARTERLY_REPORT_YEAR = os.environ["QUARTERLY_REPORT_YEAR"]
QUARTERLY_REPORT_QUARTER = os.environ["QUARTERLY_REPORT_QUARTER"]

QUARTERLY_REPORT_STATEMENTS_DIR: Path = Path(
    QUARTERLY_REPORT_ROOT_DIR
    / Path(QUARTERLY_REPORT_YEAR)
    / Path("Q" + QUARTERLY_REPORT_QUARTER)
    / Path("raw")
)
QUARTERLY_REPORT_EXPORT_FILENAME = f"{date.today().strftime('%Y-%m-%d')} {QUARTERLY_REPORT_BASE_FILENAME} {QUARTERLY_REPORT_YEAR}Q{QUARTERLY_REPORT_QUARTER}.{QUARTERLY_REPORT_FILE_EXTENSION}"


@dataclass
class StatementConfig:
    """Configuration class that holds all the necessary parameters to
    read in and transform the statement data.

    name (str): name of the account/statement
    full_path (str): is initialized based on relative location and from static information and the name
    dateformat (str): the format of the date fields
    map_column_names(dict[str, str]): mapping to rename columns to canonical names
    validation_model (DataFrameModel): the class of the pandera validation model

    reading_delimiter (str): delimiting character for the csv-reader
    reading_skiprows (int): rows to skip for the csv-reader
    reading_thousands (str): thousands delimiter for the csv-reader
    reading_quotechar (str): quotechar for the csv-reader
    reading_decimal (str): decimal delimiter for the csv-reader
    """

    name: str
    full_path: Path = field(init=False)
    dateformat: str
    map_column_names: dict[str, str]
    validation_model: pa.DataFrameModel

    reading_delimiter: str = ","
    reading_skiprows: int = 0
    reading_thousands: str = "."
    reading_quotechar: str = '"'
    reading_decimal: str = ","

    def __post_init__(self):
        """

        Initiailze the 'full_path' based on the execution parameters of 'year', 'quarter' and the 'base dir'
        and adding the 'name' to create a fully fledged export path
        """
        self.full_path = (
            QUARTERLY_REPORT_STATEMENTS_DIR
            / f"{QUARTERLY_REPORT_YEAR}Q{QUARTERLY_REPORT_QUARTER} - {self.name}.csv"
        )
