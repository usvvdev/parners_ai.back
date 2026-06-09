# application dependencies

from .base import BaseAPIClient

from ....domain.types import OfferSummary


class OfferAPIClient(BaseAPIClient):
    async def fetch_all(self) -> list[OfferSummary]:
        data = await self._get("/offers")

        return [OfferSummary.model_validate(item) for item in data]

    async def fetch_by_id(self, id: int) -> OfferSummary:
        data = await self._get(f"/offers/{id}")

        return OfferSummary.model_validate(data)

    async def create(
        self,
        payload: dict,
    ) -> OfferSummary:
        data = await self._post(
            "/offers",
            json=payload,
        )

        return OfferSummary.model_validate(data)

    async def update(
        self,
        id: int,
        payload: dict,
    ) -> OfferSummary:
        data = await self._patch(
            f"/offers/{id}",
            json=payload,
        )

        return OfferSummary.model_validate(data)

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._delete(f"/offers/{id}")
