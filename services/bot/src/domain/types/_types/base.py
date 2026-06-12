# packages

from typing import Generic, TypeVar, Any

from pydantic import BaseModel, Field

from libs.domain.types._types.common import BaseModelType


class BaseFetch(BaseModelType):
    id: int = Field(
        ...,
        description="ID сущности",
    )


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T] = Field(default_factory=list)
    total: int = Field(...)
    page: int = Field(...)
    size: int = Field(...)
    pages: int = Field(...)


def parse_nested_page(
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

    return PaginatedResponse(
        items=[model.model_validate(item) for item in data.get("items", [])],
        total=data.get("total", 0),
        page=data.get("page", 1),
        size=data.get("size", 0),
        pages=data.get("pages", 0),
    )
