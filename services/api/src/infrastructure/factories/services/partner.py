# packages

from pathlib import Path

# application dependencies

from libs.infrastructure.factories.stores.mysql import (
    MySQLEngineFactory,
    MySQLPartnerRepository,
)

from ....interface.services import PartnerRepositoryService

from libs.infrastructure.factories.common import ApplicationConfigFactory


class PartnerRepositoryServiceFactory:
    @staticmethod
    def create() -> MySQLPartnerRepository:
        config = ApplicationConfigFactory.create(
            service_dir=Path(__file__).parents[4],
        )

        repository = MySQLPartnerRepository.create(
            engine=MySQLEngineFactory.create(
                config=config,
            ),
        )

        return PartnerRepositoryService(
            repository=repository,
        )
