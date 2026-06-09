# packages

from dataclasses import dataclass

from httpx import AsyncClient

# application dependencies

from ..clients.api import (
    PartnerAPIClient,
    LinkAPIClient,
    OfferAPIClient,
)


@dataclass(frozen=True)
class APIClients:
    http: AsyncClient
    partner: PartnerAPIClient
    link: LinkAPIClient
    offer: OfferAPIClient

    async def close(self) -> None:
        await self.http.aclose()


class APIClientsFactory:
    @staticmethod
    def create(
        base_url: str,
        timeout: float = 30.0,
    ) -> APIClients:
        http = AsyncClient(
            base_url=base_url,
            timeout=timeout,
        )

        return APIClients(
            http=http,
            partner=PartnerAPIClient(client=http),
            link=LinkAPIClient(client=http),
            offer=OfferAPIClient(client=http),
        )
