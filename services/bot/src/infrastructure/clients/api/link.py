# application dependencies

from .base import BaseAPIClient

from ....domain.types import LinkDetail


class LinkAPIClient(BaseAPIClient):
    async def fetch_by_id(self, id: int) -> LinkDetail:
        data = await self._get(f"/links/{id}")

        return LinkDetail.model_validate(data)

    async def update(
        self,
        id: int,
        payload: dict,
    ) -> LinkDetail:
        data = await self._patch(
            f"/links/{id}",
            json=payload,
        )

        return LinkDetail.model_validate(data)
