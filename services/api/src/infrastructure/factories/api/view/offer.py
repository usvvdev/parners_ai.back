from fastapi import Depends

from .....interface.api.views import OfferRepositoryView

from .....interface.services import OfferRepositoryService

from ...services import OfferRepositoryServiceFactory


class OfferRepositoryViewFactory:
    @staticmethod
    def create(
        service: OfferRepositoryService = Depends(
            OfferRepositoryServiceFactory.create,
        ),
    ) -> OfferRepositoryView:
        return OfferRepositoryView(
            service=service,
        )
