from fastapi import (
    APIRouter,
    Depends,
)

from ..dto import (
    FetchOffer,
    InsertOffer,
)

from ..views.offer import (
    OfferRepositoryView,
)

from ....infrastructure.factories.services import OfferRepositoryServiceFactory


offer_router = APIRouter(
    prefix="/offers",
    tags=["offer"],
)


@offer_router.get("/")
async def fetch_offers(
    view: OfferRepositoryView = Depends(
        OfferRepositoryServiceFactory.create,
    ),
) -> list[FetchOffer]:
    return await view.fetch()


@offer_router.post("/")
async def create_offer(
    data: InsertOffer,
    view: OfferRepositoryView = Depends(
        OfferRepositoryServiceFactory.create,
    ),
) -> FetchOffer:
    return await view.create(
        data=data,
    )


@offer_router.delete("/{offer_id}")
async def delete_offer(
    offer_id: int,
    view: OfferRepositoryView = Depends(
        OfferRepositoryServiceFactory.create,
    ),
) -> FetchOffer:
    return await view.delete(
        offer_id=offer_id,
    )
