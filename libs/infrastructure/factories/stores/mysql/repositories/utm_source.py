from ..engine import MySQLEngineFactory

from libs.infrastructure.stores.mysql.repositories import UTMSourceRepository


class UTMSourceRepositoryFactory:
    @staticmethod
    def create(
        engine: MySQLEngineFactory,
    ) -> UTMSourceRepository:
        return UTMSourceRepository(
            engine=engine,
        )
