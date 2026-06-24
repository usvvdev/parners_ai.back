from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import (
    Page,
    Params,
    paginate,
)

from ..dto import (
    FetchOfferPosition,
    InsertOfferPosition,
    FiltersOfferPosition,
)

from ..views import OfferPositionRepositoryView

from ....infrastructure.utils.functions import (
    verify_token,
    set_custom_pagination,
)

from ....infrastructure.utils.decorators import disable_extension_check

from ....infrastructure.factories.api.view import OfferPositionRepositoryViewFactory


offer_position_router = APIRouter(
    prefix="/offer-positions",
    tags=["Offer Positions"],
)


@offer_position_router.get(
    "",
    response_model=Page[FetchOfferPosition],
)
@disable_extension_check
async def fetch(
    view: OfferPositionRepositoryView = Depends(
        OfferPositionRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
    params: Params = Depends(
        set_custom_pagination,
    ),
    filters: FiltersOfferPosition = Depends(),
) -> Page[FetchOfferPosition]:
    data = await view.fetch(
        filters=filters,
    )

    return paginate(
        data,
        params=params,
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
