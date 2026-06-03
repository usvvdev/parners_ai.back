from fastapi import (
    APIRouter,
    Depends,
)

from ..dto import (
    FetchPartner,
    FetchPartnerLinks,
    InsertPartner,
)

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
) -> FetchPartnerLinks:
    return await view.fetch_by_id(
        id=id,
    )


@partner_router.post("/")
async def create_partner(
    data: InsertPartner,
    view: PartnerRepositoryView = Depends(
        PartnerRepositoryViewFactory.create,
    ),
) -> FetchPartner:
    return await view.insert(
        data=data,
    )


@partner_router.delete("/{id}")
async def delete_offer(
    id: int,
    view: PartnerRepositoryView = Depends(
        PartnerRepositoryViewFactory.create,
    ),
):
    return await view.delete(
        id=id,
    )
