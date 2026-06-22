# application depencies

from ....interface.services import PartnerService

from libs.domain.types._types.shared import APIClients


class PartnerServiceFactory:
    @staticmethod
    def create(
        clients: APIClients,
    ) -> PartnerService:
        return PartnerService(
            partner_client=clients.partner,
            link_client=clients.link,
            utm_source_client=clients.utm_source,
        )
