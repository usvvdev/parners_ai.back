from fastapi import Depends

from ..base import create_mysql_engine

from .....interface.api.views import PartnerRepositoryView

from libs.infrastructure.stores.mysql import MySQLEngine

from libs.infrastructure.stores.mysql.repositories import PartnerRepository

from libs.infrastructure.factories.stores.mysql.repositories import (
    PartnerRepositoryFactory,
)


class PartnerRepositoryViewFactory:
    @staticmethod
    def create(
        engine: MySQLEngine = Depends(
            create_mysql_engine,
        ),
    ) -> PartnerRepositoryView:
        repository: PartnerRepository = PartnerRepositoryFactory.create(
            engine=engine,
        )
        return PartnerRepositoryView(
            repository=repository,
        )
