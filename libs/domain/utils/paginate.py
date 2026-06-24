# packages

from typing import Any

# application dependencies

from libs.domain.types._types.common import BaseModelType

from libs.domain.types._types.shared import PaginatedResponse


def parse_paginated_response(
    data: Any,
    model: type[BaseModelType],
) -> PaginatedResponse[BaseModelType]:
    if isinstance(data, PaginatedResponse):
        return data

    if not isinstance(data, dict):
        return PaginatedResponse(
            items=[],
            total=0,
            page=1,
            size=0,
            pages=0,
        )

    items = [
        model.model_validate(
            item,
        )
        for item in data.get("items", [])
    ]

    return PaginatedResponse(
        items=items,
        total=data.get("total", 0),
        page=data.get("page", 1),
        size=data.get("size", 0),
        pages=data.get("pages", 0),
    )
