from ..engine import ClickhouseEngineFactory

from libs.infrastructure.stores.clickhouse.repositories import OfferPositionRepository


class OfferPositionRepositoryFactory:
    @staticmethod
    def create(
        engine: ClickhouseEngineFactory,
    ) -> OfferPositionRepository:
        return OfferPositionRepository(
            engine=engine,
        )
