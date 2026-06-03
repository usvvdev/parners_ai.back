from typing import Any

from fastapi import (
    APIRouter,
    Depends,
)

from ..dto import FetchPartner

from ..views import PartnerRepositoryView

from ....infrastructure.factories.api.view import PartnerRepositoryViewFactory


partner_router = APIRouter(
    prefix="/partners",
    tags=["Partners"],
)


@partner_router.get("/")
async def fetch_offers(
    view: PartnerRepositoryView = Depends(
        PartnerRepositoryViewFactory.create,
    ),
) -> list[FetchPartner]:
    return await view.fetch()


@partner_router.get("/{id}")
async def fetch_partner(
    id: int,
    view: PartnerRepositoryView = Depends(
        PartnerRepositoryViewFactory.create,
    ),
) -> FetchPartner | None:
    return await view.fetch_by_id(
        id=id,
    )
