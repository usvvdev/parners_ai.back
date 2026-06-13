# packages

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import (
    Page,
    Params,
    paginate,
)

# application depencies

from ..dto import (
    FetchOffer,
    FetchOffers,
    InsertOffer,
    UpdateOffer,
)

from ..views import OfferRepositoryView

from ....infrastructure.utils.functions import (
    verify_token,
    set_custom_pagination,
)

from ....infrastructure.utils.decorators import disable_extension_check

from ....infrastructure.factories.api.view import OfferRepositoryViewFactory


offer_router = APIRouter(
    prefix="/offers",
    tags=["Offers"],
)


@offer_router.get(
    "",
    response_model=Page[FetchOffers],
)
@disable_extension_check
async def fetch_offers(
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
    params: Params = Depends(
        set_custom_pagination,
    ),
) -> Page[FetchOffers]:
    data = await view.fetch()

    return paginate(
        data,
        params=params,
    )


@offer_router.post("")
async def create_offer(
    data: InsertOffer,
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
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
    _: str = Depends(
        verify_token,
    ),
) -> FetchOffer:
    return await view.fetch_by_id(
        id=id,
    )


@offer_router.patch("/{id}")
async def update_offer(
    id: int,
    data: UpdateOffer,
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
) -> FetchOffer:
    return await view.update(
        id=id,
        data=data,
    )


@offer_router.delete("/{id}")
async def delete_offer(
    id: int,
    view: OfferRepositoryView = Depends(
        OfferRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
) -> None:
    return await view.delete(
        id=id,
    )
