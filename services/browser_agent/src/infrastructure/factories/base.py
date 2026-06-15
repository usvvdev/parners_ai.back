# packages

from httpx import AsyncClient

from pydantic import ConfigDict

from ..clients.api import (
    LinkAPIClient,
    OfferAPIClient,
    PartnerAPIClient,
    UTMSourceAPIClient,
    OfferPositionAPIClient,
)

from libs.core.config import TApplicationConfig
from libs.domain.types._types.common import BaseModelType


class APIClients(BaseModelType):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=True,
    )

    http: AsyncClient
    link: LinkAPIClient
    offer: OfferAPIClient
    partner: PartnerAPIClient
    utm_source: UTMSourceAPIClient
    offer_position: OfferPositionAPIClient

    async def close(self) -> None:
        await self.http.aclose()


class APIClientsFactory:
    @staticmethod
    def create(
        config: type[TApplicationConfig],
        timeout: float = 60.0,
    ) -> APIClients:
        http = AsyncClient(
            base_url=config.api_options.base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {config.access_token}",
            },
        )

        return APIClients(
            http=http,
            link=LinkAPIClient(client=http),
            offer=OfferAPIClient(client=http),
            partner=PartnerAPIClient(client=http),
            utm_source=UTMSourceAPIClient(client=http),
            offer_position=OfferPositionAPIClient(client=http),
        )
