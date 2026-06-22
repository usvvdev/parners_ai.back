# packages

from typing import (
    Generic,
    TypeVar,
)

from pydantic import Field

# application dependencies

from ..common.model import BaseModelType


T = TypeVar("T")


class PaginatedResponse(
    BaseModelType,
    Generic[T],
):
    items: list[T] = Field(
        default_factory=list,
        description="",
    )

    total: int = Field(
        ...,
        description="",
    )

    page: int = Field(
        ...,
        description="",
    )

    size: int = Field(
        ...,
        description="",
    )

    pages: int = Field(
        ...,
        description="",
    )


class BaseFetchType(BaseModelType):
    id: int = Field(
        ...,
        description="ID сущности",
    )
