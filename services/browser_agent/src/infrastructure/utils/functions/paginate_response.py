# application dependencies

from ....domain.types._types.base import PaginatedResponse

from libs.domain.types._types.common import BaseModelType


def parse_paginated_response(
    data: dict,
    model: type[BaseModelType],
) -> PaginatedResponse[BaseModelType]:
    return PaginatedResponse(
        items=[model.model_validate(item) for item in data["items"]],
        total=data["total"],
        page=data["page"],
        size=data["size"],
        pages=data["pages"],
    )
