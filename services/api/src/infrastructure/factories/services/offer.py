# packages

from pathlib import Path

# application dependencies

from libs.infrastructure.factories.stores.mysql import (
    MySQLEngineFactory,
    MySQLOfferRepository,
)

from ....interface.services import OfferRepositoryService

from libs.infrastructure.factories.common import ApplicationConfigFactory


class OfferRepositoryServiceFactory:
    @staticmethod
    def create() -> OfferRepositoryService:
        config = ApplicationConfigFactory.create(
            service_dir=Path(__file__).parent.parent,
        )

        repository = MySQLOfferRepository.create(
            engine=MySQLEngineFactory.create(
                config=config,
            ),
        )

        return OfferRepositoryService(
            repository=repository,
        )
