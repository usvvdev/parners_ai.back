# packages

from httpx import AsyncClient

# application dependencies

from ..clients.api import (
    PartnerAPIClient,
    LinkAPIClient,
    OfferAPIClient,
)

from libs.core.config import TApplicationConfig

from libs.domain.types._types.common import BaseModelType


class APIClients(BaseModelType):
    http: AsyncClient
    partner: PartnerAPIClient
    link: LinkAPIClient
    offer: OfferAPIClient

    async def close(self) -> None:
        await self.http.aclose()


class APIClientsFactory:
    @staticmethod
    def create(
        config: type[TApplicationConfig],
        timeout: float = 30.0,
    ) -> APIClients:
        http = AsyncClient(
            base_url=config.telegram_options.api_base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {config.access_token}",
            },
        )

        return APIClients(
            http=http,
            partner=PartnerAPIClient(client=http),
            link=LinkAPIClient(client=http),
            offer=OfferAPIClient(client=http),
        )
