from pathlib import Path

from loguru import logger

from alembic import command

from alembic.config import Config


def run_migrations(
    path: Path,
) -> None:
    config = Config(path / "alembic.ini")
    config.set_main_option(
        "script_location",
        str(path / "migrations"),
    )
    command.revision(config, autogenerate=True)
    logger.info("Genereted version for the table")
    command.upgrade(config, "head")
    logger.info("Updraded version of the table")
