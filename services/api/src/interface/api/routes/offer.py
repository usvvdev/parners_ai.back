from fastapi import (
    APIRouter,
    Depends,
)

from ..dto import (
    FetchOffer,
    FetchOffers,
    InsertOffer,
)

from ..views import OfferRepositoryView

from ....infrastructure.factories.api.view import OfferRepositoryViewFactory


offer_router = APIRouter(
    prefix="/offers",
    tags=["Offers"],
)


@offer_router.get(
    "",
    response_model=list[FetchOffers],
)
async def fetch_offers(
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
) -> list[FetchOffers]:
    return await view.fetch()


@offer_router.post("")
async def create_offer(
    data: InsertOffer,
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
) -> FetchOffer:
    return await view.insert(
        data=data,
    )


@offer_router.get(
    "/{id}",
    response_model=FetchOffer,
)
async def fetch_offer_by_id(
    id: int,
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
) -> FetchOffer:
    return await view.fetch_by_id(
        id=id,
    )


@offer_router.put("/{id}")
async def update_offer(
    id: int,
    data: InsertOffer,
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
) -> FetchOffer:
    return await view.update(
        id=id,
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
