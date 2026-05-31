# application depencies

from libs.core.config import TApplicationConfig

from libs.infrastructure.stores.mysql import MySQLEngine


class MySQLEngineFactory:
    @staticmethod
    def create(
        config: type[TApplicationConfig],
    ) -> MySQLEngine:
        return MySQLEngine(
            config=config,
        )
