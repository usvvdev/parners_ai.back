from pathlib import Path

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
    command.upgrade(config, "head")
