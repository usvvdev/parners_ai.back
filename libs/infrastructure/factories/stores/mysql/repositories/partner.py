from ..engine import MySQLEngineFactory

from libs.infrastructure.stores.mysql.repositories import PartnerRepository


class PartnerRepositoryFactory:
    @staticmethod
    def create(
        engine: MySQLEngineFactory,
    ) -> PartnerRepository:
        return PartnerRepository(
            engine=engine,
        )
