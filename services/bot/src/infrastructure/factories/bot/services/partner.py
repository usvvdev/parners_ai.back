# application depencies

from .....interface.services import PartnerService

from ...base import APIClients


class PartnerServiceFactory:
    @staticmethod
    def create(
        clients: APIClients,
    ) -> PartnerService:
        return PartnerService(
            partner_client=clients.partner,
            link_client=clients.link,
        )
