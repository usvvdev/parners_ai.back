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
    FetchPartner,
    FetchPartners,
    InsertPartner,
    UpdatePartner,
)

from ..views import PartnerRepositoryView

from ....infrastructure.utils.functions import set_custom_pagination

from ....infrastructure.utils.decorators import disable_extension_check

from ....infrastructure.factories.api.view import PartnerRepositoryViewFactory


partner_router = APIRouter(
    prefix="/partners",
    tags=["Partners"],
)


@partner_router.get(
    "",
    response_model=Page[FetchPartner],
)
@disable_extension_check
async def fetch_offers(
    view: PartnerRepositoryView = Depends(
        PartnerRepositoryViewFactory.create,
    ),
    pagination_params: Params = Depends(
        set_custom_pagination,
    ),
) -> Page[FetchPartner]:
    data = await view.fetch()

    return paginate(
        data,
        params=pagination_params,
    )


@partner_router.get(
    "/{id}",
    response_model=FetchPartners,
)
async def fetch_partner(
    id: int,
    view: PartnerRepositoryView = Depends(
        PartnerRepositoryViewFactory.create,
    ),
) -> FetchPartners:
    return await view.fetch_by_id(
        id=id,
    )


@partner_router.post(
    "",
    response_model=FetchPartners,
)
async def create_partner(
    data: InsertPartner,
    view: PartnerRepositoryView = Depends(
        PartnerRepositoryViewFactory.create,
    ),
) -> FetchPartners:
    return await view.insert(
        data=data,
    )


@partner_router.patch(
    "/{id}",
    response_model=FetchPartners,
)
async def update_partner(
    id: int,
    data: UpdatePartner,
    view: PartnerRepositoryView = Depends(
        PartnerRepositoryViewFactory.create,
    ),
) -> FetchPartners:
    return await view.update(
        id=id,
        data=data,
    )


@partner_router.delete("/{id}")
async def delete_partner(
    id: int,
    view: PartnerRepositoryView = Depends(
        PartnerRepositoryViewFactory.create,
    ),
) -> None:
    return await view.delete(
        id=id,
    )
