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
    FetchUTMSource,
    FetchUTMSources,
    InsertUTMSource,
    UpdateUTMSource,
)

from ..views import UTMSourceRepositoryView

from ....infrastructure.utils.functions import set_custom_pagination

from ....infrastructure.utils.decorators import disable_extension_check

from ....infrastructure.factories.api.view import UTMSourceRepositoryViewFactory


utm_source_router = APIRouter(
    prefix="/utm-sources",
    tags=["UTM Sources"],
)


@utm_source_router.get(
    "",
    response_model=Page[FetchUTMSources],
)
@disable_extension_check
async def fetch_utm_sources(
    view: UTMSourceRepositoryView = Depends(
        UTMSourceRepositoryViewFactory.create,
    ),
    pagination_params: Params = Depends(
        set_custom_pagination,
    ),
) -> Page[FetchUTMSources]:
    data = await view.fetch()

    return paginate(
        data,
        params=pagination_params,
    )


@utm_source_router.post("")
async def create_utm_source(
    data: InsertUTMSource,
    view: UTMSourceRepositoryView = Depends(
        UTMSourceRepositoryViewFactory.create,
    ),
) -> FetchUTMSource:
    return await view.insert(
        data=data,
    )


@utm_source_router.get(
    "/{id}",
    response_model=FetchUTMSource,
)
async def fetch_utm_source_by_id(
    id: int,
    view: UTMSourceRepositoryView = Depends(
        UTMSourceRepositoryViewFactory.create,
    ),
) -> FetchUTMSource:
    return await view.fetch_by_id(
        id=id,
    )


@utm_source_router.patch("/{id}")
async def update_utm_source(
    id: int,
    data: UpdateUTMSource,
    view: UTMSourceRepositoryView = Depends(
        UTMSourceRepositoryViewFactory.create,
    ),
) -> FetchUTMSource:
    return await view.update(
        id=id,
        data=data,
    )


@utm_source_router.delete("/{id}")
async def delete_utm_source(
    id: int,
    view: UTMSourceRepositoryView = Depends(
        UTMSourceRepositoryViewFactory.create,
    ),
) -> None:
    return await view.delete(
        id=id,
    )
