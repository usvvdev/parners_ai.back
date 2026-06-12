from fastapi import (
    APIRouter,
    Depends,
)

from ..dto import (
    FetchOfferPosition,
    InsertOfferPosition,
    FiltersOfferPosition,
)

from ..views import OfferPositionRepositoryView

from ....infrastructure.utils.functions import verify_token

from ....infrastructure.factories.api.view import OfferPositionRepositoryViewFactory


offer_position_router = APIRouter(
    prefix="/offer-positions",
    tags=["Offer Positions"],
)


@offer_position_router.get(
    "",
    response_model=list[FetchOfferPosition],
)
async def fetch(
    filters: FiltersOfferPosition = Depends(),
    view: OfferPositionRepositoryView = Depends(
        OfferPositionRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
) -> list[FetchOfferPosition]:
    return await view.fetch(
        filters=filters,
    )


@offer_position_router.post(
    "",
    response_model=FetchOfferPosition,
)
async def create_offer_position(
    data: InsertOfferPosition,
    view: OfferPositionRepositoryView = Depends(
        OfferPositionRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
) -> FetchOfferPosition:
    return await view.insert(
        data=data,
    )
