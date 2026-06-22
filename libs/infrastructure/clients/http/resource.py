# packages

from typing import (
    Any,
    Generic,
)

# application depencies

from ..base import (
    TList,
    TDetail,
)

from .client import BaseHTTPClient

from libs.domain.types._types.shared import (
    Params,
    PaginatedResponse,
)

from libs.core.constants import DEFAULT_PAGE_SIZE

from libs.domain.utils import parse_paginated_response

from libs.domain.types._types.common import BaseModelType

from libs.domain.protocols.http import IHTTPClientProtocol


class BaseResourceAPIClient(
    IHTTPClientProtocol,
    Generic[TList, TDetail],
):
    path: str

    list_schema: type[TList]
    detail_schema: type[TDetail]

    detail_paginated: bool = True

    def __init__(
        self,
        *,
        client: BaseHTTPClient,
    ) -> None:
        self._client = client

    def _generate_params(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        params = {}

        if page is not None and size is not None:
            params.update(
                Params(
                    page=page,
                    size=size,
                ).dump
            )

        if filters:
            params.update(filters)

        return params or None

    async def fetch_page(
        self,
        *,
        page: int = 1,
        size: int = DEFAULT_PAGE_SIZE,
        filters: dict[str, Any] | None = None,
    ) -> PaginatedResponse[TList]:
        response = await self._client.get(
            self.path,
            params=self._generate_params(
                page=page,
                size=size,
                filters=filters,
            ),
        )

        return parse_paginated_response(
            response,
            self.list_schema,
        )

    async def fetch_all(
        self,
        *,
        size: int = DEFAULT_PAGE_SIZE,
        filters: dict[str, Any] | None = None,
    ) -> list[TList]:
        items: list[TList] = []
        page = 1

        while True:
            result = await self.fetch_page(
                page=page,
                size=size,
                filters=filters,
            )

            items.extend(result.items)

            if page >= result.pages:
                return items

            page += 1

    async def fetch_by_id(
        self,
        id: int,
        *,
        page: int = 1,
        size: int = DEFAULT_PAGE_SIZE,
        paginated: bool | None = None,
    ) -> TDetail:
        use_pagination = self.detail_paginated if paginated is None else paginated

        response = await self._client.get(
            f"{self.path}/{id}",
            params=(
                self._generate_params(
                    page=page,
                    size=size,
                )
                if use_pagination
                else None
            ),
        )

        return self.detail_schema.model_validate(
            response,
        )

    async def create(
        self,
        data: BaseModelType,
    ) -> TDetail:
        response = await self._client.post(
            self.path,
            json=data.dump,
        )

        return self.detail_schema.model_validate(
            response,
        )

    async def update(
        self,
        id: int,
        data: BaseModelType,
    ) -> TDetail:
        response = await self._client.patch(
            f"{self.path}/{id}",
            json=data.dump,
        )

        return self.detail_schema.model_validate(
            response,
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._client.delete(
            f"{self.path}/{id}",
        )
