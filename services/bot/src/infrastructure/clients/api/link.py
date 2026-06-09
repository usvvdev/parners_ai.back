# application dependencies

from .base import BaseAPIClient

from ....domain.types import LinkSummary, LinkDetail


class LinkAPIClient(BaseAPIClient):
    async def fetch_all(self) -> list[LinkSummary]:
        data = await self._get("/links")

        return [LinkSummary.model_validate(item) for item in data]

    async def fetch_by_id(self, id: int) -> LinkDetail:
        data = await self._get(f"/links/{id}")

        return LinkDetail.model_validate(data)

    async def create(
        self,
        payload: dict,
    ) -> LinkDetail:
        data = await self._post(
            "/links",
            json=payload,
        )

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

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._delete(f"/links/{id}")
