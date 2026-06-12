# packages

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import (
    Page,
    paginate,
)

# application depencies

from ..dto import (
    FetchLink,
    FetchLinks,
    InsertLink,
    UpdateLink,
)

from ..views import LinkRepositoryView

from libs.core.constants import DEFAULT_LIST_PARAMS

from ....infrastructure.utils.functions import verify_token

from ....infrastructure.utils.decorators import disable_extension_check

from ....infrastructure.factories.api.view import LinkRepositoryViewFactory


link_router = APIRouter(
    prefix="/links",
    tags=["Links"],
)


@link_router.get(
    "",
    response_model=Page[FetchLinks],
)
@disable_extension_check
async def fetch_links(
    view: LinkRepositoryView = Depends(
        LinkRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
) -> Page[FetchLinks]:
    data = await view.fetch()

    return paginate(
        data,
        params=DEFAULT_LIST_PARAMS,
    )


@link_router.get(
    "/{id}",
    response_model=FetchLink,
)
async def fetch_link_by_id(
    id: int,
    view: LinkRepositoryView = Depends(
        LinkRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
) -> FetchLink:
    return await view.fetch_by_id(
        id=id,
        params=DEFAULT_LIST_PARAMS,
    )


@link_router.post("")
async def create_link(
    data: InsertLink,
    view: LinkRepositoryView = Depends(
        LinkRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
) -> FetchLink:
    return await view.insert(
        data=data,
    )


@link_router.patch("/{id}")
async def update_link(
    id: int,
    data: UpdateLink,
    view: LinkRepositoryView = Depends(
        LinkRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
) -> FetchLink:
    return await view.update(
        id=id,
        data=data,
    )


@link_router.delete("/{id}")
async def delete_link(
    id: int,
    view: LinkRepositoryView = Depends(
        LinkRepositoryViewFactory.create,
    ),
    _: str = Depends(
        verify_token,
    ),
) -> None:
    return await view.delete(
        id=id,
    )
