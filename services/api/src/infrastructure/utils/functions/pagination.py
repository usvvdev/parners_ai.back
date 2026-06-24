from fastapi_pagination import Params

from libs.core.constants import (
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
)


def set_custom_pagination(
    page: int = DEFAULT_PAGE,
    size: int = DEFAULT_PAGE_SIZE,
) -> Params:
    return Params(
        page=page,
        size=size,
    )
