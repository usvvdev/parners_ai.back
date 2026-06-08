from fastapi import Depends

from ..base import create_clickhouse_engine

from .....interface.api.views import OfferPositionRepositoryView

from libs.infrastructure.stores.clickhouse import ClickHouseEngine

from libs.infrastructure.stores.clickhouse.repositories import OfferPositionRepository

from libs.infrastructure.factories.stores.clickhouse.repositories import (
    OfferPositionRepositoryFactory,
)


class OfferPositionRepositoryViewFactory:
    @staticmethod
    def create(
        engine: ClickHouseEngine = Depends(
            create_clickhouse_engine,
        ),
    ) -> OfferPositionRepositoryView:
        repository: OfferPositionRepository = OfferPositionRepositoryFactory.create(
            engine=engine,
        )
        return OfferPositionRepositoryView(
            repository=repository,
        )
