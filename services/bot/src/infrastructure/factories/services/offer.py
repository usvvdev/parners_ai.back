# application depencies

from ....interface.services import OfferService

from libs.domain.types._types.shared import APIClients


class OfferServiceFactory:
    @staticmethod
    def create(
        clients: APIClients,
    ) -> OfferService:
        return OfferService(
            offer_client=clients.offer,
            link_client=clients.link,
        )
