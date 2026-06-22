# packages

from httpx import AsyncClient

# application depencies

from libs.core.config import TApplicationConfig

from libs.domain.types._types.shared import APIClients

from libs.infrastructure.clients.http.client import BaseHTTPClient

from libs.infrastructure.clients.http.repositories import CLIENTS


class APIClientsFactory:
    @staticmethod
    def create(
        config: type[TApplicationConfig],
        timeout: float = 60.0,
    ) -> APIClients:
        http_client = AsyncClient(
            base_url=config.api_options.base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {config.access_token}",
            },
        )

        client = BaseHTTPClient(
            client=http_client,
        )

        return APIClients(
            client=client,
            **{name: cls(client=client) for name, cls in CLIENTS.items()},
        )
