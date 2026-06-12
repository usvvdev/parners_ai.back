# application depencies

from .....interface.services import LinkService

from ...base import APIClients


class LinkServiceFactory:
    @staticmethod
    def create(
        clients: APIClients,
    ) -> LinkService:
        return LinkService(
            link_client=clients.link,
            partner_client=clients.partner,
            offer_client=clients.offer,
        )
