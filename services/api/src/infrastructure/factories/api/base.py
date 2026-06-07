# packages

from pathlib import Path

# application dependencies

from libs.infrastructure.factories.stores.mysql import MySQLEngineFactory

from libs.infrastructure.factories.common import ApplicationConfigFactory


def create_mysql_engine() -> MySQLEngineFactory:
    config = ApplicationConfigFactory.create(
        service_dir=Path(__file__).parents[4],
    )

    return MySQLEngineFactory.create(
        config=config,
    )
