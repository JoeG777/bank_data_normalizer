import logging
from src.controller import Controller
from src.config import StatementConfig

from src.statement import (
    amex_statement_config,
    dkb_statement_config,
    mm_statement_config,
    pp_statement_config,
)


logging.basicConfig(
    filename="info.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m-%d-%Y %H:%M:%S",
)


def main(export_flag: bool = False) -> None:

    statements: list[StatementConfig] = [
        StatementConfig(**dkb_statement_config),
        StatementConfig(**amex_statement_config),
        StatementConfig(**pp_statement_config),
        StatementConfig(**mm_statement_config),
    ]

    df = Controller.process_statements(statements)

    # create additional columns with custom logic and validate
    df_final = Controller.add_custom_columns(df)
    Controller.validate_canonical_data_model(df_final)
    if export_flag:
        Controller.export_data(df_final)


if __name__ == "__main__":
    main(export_flag=True)
