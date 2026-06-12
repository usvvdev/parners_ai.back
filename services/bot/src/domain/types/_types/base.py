# packages

from typing import Generic, TypeVar

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
