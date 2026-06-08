from fastapi import (
    APIRouter,
    Depends,
)

from ..dto import (
    FetchLink,
    FetchLinks,
    InsertLink,
    UpdateLink,
)

from ..views import LinkRepositoryView

from ....infrastructure.factories.api.view import LinkRepositoryViewFactory


link_router = APIRouter(
    prefix="/links",
    tags=["Links"],
)


@link_router.get(
    "",
    response_model=list[FetchLinks],
)
async def fetch_links(
    view: LinkRepositoryView = Depends(
        LinkRepositoryViewFactory.create,
    ),
) -> list[FetchLinks]:
    return await view.fetch()


@link_router.post("")
async def create_link(
    data: InsertLink,
    view: LinkRepositoryView = Depends(
        LinkRepositoryViewFactory.create,
    ),
) -> FetchLink:
    return await view.insert(
        data=data,
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
) -> FetchLink:
    return await view.fetch_by_id(
        id=id,
    )


@link_router.patch("/{id}")
async def update_link(
    id: int,
    data: UpdateLink,
    view: LinkRepositoryView = Depends(
        LinkRepositoryViewFactory.create,
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
) -> FetchLink:
    return await view.delete(
        id=id,
    )
