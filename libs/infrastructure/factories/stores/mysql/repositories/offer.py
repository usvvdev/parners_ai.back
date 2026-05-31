from ..engine import MySQLEngineFactory

from libs.infrastructure.stores.mysql.repositories import OfferRepository


class MySQLOfferRepository:
    @staticmethod
    def create(
        engine: MySQLEngineFactory,
    ) -> OfferRepository:
        return OfferRepository(
            engine=engine,
        )
