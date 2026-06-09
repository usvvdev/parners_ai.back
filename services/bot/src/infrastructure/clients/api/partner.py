# application dependencies

from .base import BaseAPIClient

from ....domain.types import Partner, PartnerDetail


class PartnerAPIClient(BaseAPIClient):
    async def fetch_all(self) -> list[Partner]:
        data = await self._get("/partners")

        return [Partner.model_validate(item) for item in data]

    async def fetch_by_id(self, id: int) -> PartnerDetail:
        data = await self._get(f"/partners/{id}")

        return PartnerDetail.model_validate(data)

    async def create(
        self,
        payload: dict,
    ) -> PartnerDetail:
        data = await self._post(
            "/partners",
            json=payload,
        )

        return PartnerDetail.model_validate(data)

    async def update(
        self,
        id: int,
        payload: dict,
    ) -> PartnerDetail:
        data = await self._patch(
            f"/partners/{id}",
            json=payload,
        )

        return PartnerDetail.model_validate(data)

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._delete(f"/partners/{id}")
