# packages

from typing import (
    Generic,
    TypeVar,
)

from ....core.constants import DEFAULT_PAGE_SIZE
from ....domain.types._types.base import PaginatedResponse
from ...utils.functions.paginate_response import parse_paginated_response
from .base import BaseAPIClient

from libs.domain.types._types.common import BaseModelType


TList = TypeVar("TList", bound=BaseModelType)
TDetail = TypeVar("TDetail", bound=BaseModelType)


class BaseResourceAPIClient(
    BaseAPIClient,
    Generic[TList, TDetail],
):
    path: str
    list_schema: type[TList]
    detail_schema: type[TDetail]
    detail_paginated: bool = True

    async def fetch_page(
        self,
        *,
        page: int = 1,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> PaginatedResponse[TList]:
        data = await self._get(
            self.path,
            params={"page": page, "size": size},
        )
        return parse_paginated_response(
            data,
            self.list_schema,
        )

    async def fetch_all(
        self,
        *,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> list[TList]:
        items: list[TList] = []
        page = 1

        while True:
            result = await self.fetch_page(
                page=page,
                size=size,
            )
            items.extend(result.items)

            if page >= result.pages:
                break

            page += 1

        return items

    async def fetch_by_id(
        self,
        id: int,
        *,
        page: int = 1,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> TDetail:
        data = await self._get(
            f"{self.path}/{id}",
            params={"page": page, "size": size},
        )
        return self.detail_schema.model_validate(data)

    async def create(
        self,
        data: BaseModelType,
    ) -> TDetail:
        response = await self._post(
            self.path,
            json=data.model_dump(
                mode="json",
                exclude_none=True,
            ),
        )
        return self.detail_schema.model_validate(response)

    async def update(
        self,
        id: int,
        data: BaseModelType,
    ) -> TDetail:
        response = await self._patch(
            f"{self.path}/{id}",
            json=data.model_dump(
                mode="json",
                exclude_unset=True,
            ),
        )
        return self.detail_schema.model_validate(response)
