# application dependencies

from .base import BaseAPIClient

from ....domain.types import OfferSummary


class OfferAPIClient(BaseAPIClient):
    async def fetch_by_id(self, id: int) -> OfferSummary:
        data = await self._get(f"/offers/{id}")

        return OfferSummary.model_validate(data)
