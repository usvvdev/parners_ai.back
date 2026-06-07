from fastapi import Depends

from ..base import create_mysql_engine

from .....interface.api.views import LinkRepositoryView

from libs.infrastructure.stores.mysql import MySQLEngine

from libs.infrastructure.stores.mysql.repositories import LinkRepository

from libs.infrastructure.factories.stores.mysql.repositories import (
    LinkRepositoryFactory,
)


class LinkRepositoryViewFactory:
    @staticmethod
    def create(
        engine: MySQLEngine = Depends(
            create_mysql_engine,
        ),
    ) -> LinkRepositoryView:
        repository: LinkRepository = LinkRepositoryFactory.create(
            engine=engine,
        )
        return LinkRepositoryView(
            repository=repository,
        )
