from ..engine import MySQLEngineFactory

from libs.infrastructure.stores.mysql.repositories import LinkRepository


class LinkRepositoryFactory:
    @staticmethod
    def create(
        engine: MySQLEngineFactory,
    ) -> LinkRepository:
        return LinkRepository(
            engine=engine,
        )
