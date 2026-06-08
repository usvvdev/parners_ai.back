# application depencies

from libs.core.config import TApplicationConfig

from libs.infrastructure.stores.clickhouse import ClickHouseEngine


class ClickhouseEngineFactory:
    @staticmethod
    def create(
        config: type[TApplicationConfig],
    ) -> ClickHouseEngine:
        return ClickHouseEngine(
            config=config,
        )
