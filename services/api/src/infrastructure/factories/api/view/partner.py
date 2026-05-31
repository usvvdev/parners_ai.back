from fastapi import Depends

from .....interface.api.views import PartnerRepositoryView

from .....interface.services import PartnerRepositoryService

from ...services import PartnerRepositoryServiceFactory


class PartnerRepositoryViewFactory:
    @staticmethod
    def create(
        service: PartnerRepositoryService = Depends(
            PartnerRepositoryServiceFactory.create,
        ),
    ) -> PartnerRepositoryView:
        return PartnerRepositoryView(
            service=service,
        )
