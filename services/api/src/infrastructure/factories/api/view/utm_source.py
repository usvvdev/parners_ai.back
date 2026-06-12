from fastapi import Depends

from ...base import create_mysql_engine

from .....interface.api.views import UTMSourceRepositoryView

from libs.infrastructure.stores.mysql import MySQLEngine

from libs.infrastructure.stores.mysql.repositories import UTMSourceRepository

from libs.infrastructure.factories.stores.mysql.repositories import (
    UTMSourceRepositoryFactory,
)


class UTMSourceRepositoryViewFactory:
    @staticmethod
    def create(
        engine: MySQLEngine = Depends(
            create_mysql_engine,
        ),
    ) -> UTMSourceRepositoryView:
        repository: UTMSourceRepository = UTMSourceRepositoryFactory.create(
            engine=engine,
        )
        return UTMSourceRepositoryView(
            repository=repository,
        )
