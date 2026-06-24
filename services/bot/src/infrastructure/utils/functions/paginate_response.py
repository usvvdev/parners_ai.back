# application dependencies

from libs.domain.types._types.common import BaseModelType

from libs.domain.types._types.shared import PaginatedResponse


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
