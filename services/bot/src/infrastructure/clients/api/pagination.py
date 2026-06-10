# packages

from typing import Any, TypeVar

# application dependencies

from ....domain.types.pagination import PaginatedResponse

from libs.domain.types._types.common import BaseModelType


TModel = TypeVar("TModel", bound=BaseModelType)

DEFAULT_PAGE_SIZE = 5


def parse_paginated_response(
    data: dict[str, Any],
    model: type[TModel],
) -> PaginatedResponse[TModel]:
    return PaginatedResponse(
        items=[model.model_validate(item) for item in data["items"]],
        total=data["total"],
        page=data["page"],
        size=data["size"],
        pages=data["pages"],
    )
