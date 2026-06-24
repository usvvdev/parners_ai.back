from fastapi import Depends

from ...base import create_mysql_engine

from .....interface.api.views import OfferRepositoryView

from libs.infrastructure.stores.mysql import MySQLEngine

from libs.infrastructure.stores.mysql.repositories import OfferRepository

from libs.infrastructure.factories.stores.mysql.repositories import (
    OfferRepositoryFactory,
)


class OfferRepositoryViewFactory:
    @staticmethod
    def create(
        engine: MySQLEngine = Depends(
            create_mysql_engine,
        ),
    ) -> OfferRepositoryView:
        repository: OfferRepository = OfferRepositoryFactory.create(
            engine=engine,
        )
        return OfferRepositoryView(
            repository=repository,
        )
