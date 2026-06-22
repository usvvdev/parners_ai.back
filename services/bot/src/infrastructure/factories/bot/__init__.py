# packages

from pydantic import (
    BaseModel,
    ConfigDict,
)

# application depencies

from ..services import (
    PartnerServiceFactory,
    LinkServiceFactory,
    OfferServiceFactory,
)

from ....interface.services import (
    PartnerService,
    LinkService,
    OfferService,
)

from libs.domain.types._types.shared import APIClients


class BotServices(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=True,
    )

    partner: PartnerService
    link: LinkService
    offer: OfferService


class BotServicesFactory:
    @staticmethod
    def create(
        clients: APIClients,
    ) -> BotServices:
        return BotServices(
            partner=PartnerServiceFactory.create(clients),
            link=LinkServiceFactory.create(clients),
            offer=OfferServiceFactory.create(clients),
        )
