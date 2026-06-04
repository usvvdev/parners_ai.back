from fastapi import Depends

from .....interface.api.views import LinkRepositoryView

from .....interface.services import LinkRepositoryService

from ...services import LinkRepositoryServiceFactory


class LinkRepositoryViewFactory:
    @staticmethod
    def create(
        service: LinkRepositoryService = Depends(
            LinkRepositoryServiceFactory.create,
        ),
    ) -> LinkRepositoryView:
        return LinkRepositoryView(
            service=service,
        )
