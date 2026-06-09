# packages

from pathlib import Path

# application dependencies

from libs.infrastructure.factories.stores.mysql import MySQLEngineFactory

from libs.infrastructure.factories.stores.clickhouse import ClickhouseEngineFactory

from libs.infrastructure.factories.common import ApplicationConfigFactory


config = ApplicationConfigFactory.create(
    service_dir=Path(__file__).parents[3],
)


def create_mysql_engine() -> MySQLEngineFactory:
    return MySQLEngineFactory.create(
        config=config,
    )


def create_clickhouse_engine() -> ClickhouseEngineFactory:
    return ClickhouseEngineFactory.create(
        config=config,
    )
