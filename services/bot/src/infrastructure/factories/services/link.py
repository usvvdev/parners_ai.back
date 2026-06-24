# application depencies

from ....interface.services import LinkService

from libs.domain.types._types.shared import APIClients


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
