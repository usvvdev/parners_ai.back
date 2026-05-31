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

from ....infrastructure.factories.api.view import OfferRepositoryViewFactory


offer_router = APIRouter(
    prefix="/offers",
    tags=["Offers"],
)


@offer_router.get("/")
async def fetch_offers(
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
) -> list[FetchOffer]:
    return await view.fetch()


@offer_router.post("/")
async def create_offer(
    data: InsertOffer,
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
) -> FetchOffer:
    return await view.create(
        data=data,
    )


@offer_router.put("/{offer_id}")
async def update_offer(
    offer_id: int,
    data: InsertOffer,
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
) -> FetchOffer:
    return await view.update(
        offer_id=offer_id,
        data=data,
    )


@offer_router.delete("/{offer_id}")
async def delete_offer(
    offer_id: int,
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
) -> FetchOffer:
    return await view.delete(
        offer_id=offer_id,
    )
