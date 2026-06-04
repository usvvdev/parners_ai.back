# packages

from pathlib import Path

# application dependencies

from libs.infrastructure.factories.stores.mysql import (
    MySQLEngineFactory,
    MySQLLinkRepository,
)

from ....interface.services import LinkRepositoryService

from libs.infrastructure.factories.common import ApplicationConfigFactory


class LinkRepositoryServiceFactory:
    @staticmethod
    def create() -> LinkRepositoryService:
        config = ApplicationConfigFactory.create(
            service_dir=Path(__file__).parents[4],
        )

        repository = MySQLLinkRepository.create(
            engine=MySQLEngineFactory.create(
                config=config,
            ),
        )

        return LinkRepositoryService(
            repository=repository,
        )
