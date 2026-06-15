# packages

from typing import Optional

from pydantic import Field, field_validator

from .base import (
    BaseFetch,
    PaginatedResponse,
    parse_nested_page,
)
from .link import FetchLinks

from libs.domain.types._types.common import BaseModelType


class InsertPartner(BaseModelType):
    wmid: str = Field(
        ...,
        description="WMID вебмастера",
    )

    utm_source_id: int = Field(
        ...,
        description="ID UTM-источника",
    )

    is_tracking: bool = Field(
        default=True,
    )

    is_selected: bool = Field(
        default=False,
    )

    link_ids: list[int] = Field(
        default_factory=list,
    )


class UpdatePartner(BaseModelType):
    link_ids: Optional[list[int]] = Field(
        default=None,
    )


class FetchPartner(BaseFetch):
    wmid: str = Field(
        ...,
    )

    utm_source: str = Field(
        default="",
    )

    is_tracking: bool = True
    is_selected: bool = False


class FetchPartners(FetchPartner):
    links: PaginatedResponse[FetchLinks] = Field(
        default_factory=lambda: PaginatedResponse(
            items=[],
            total=0,
            page=1,
            size=0,
            pages=0,
        ),
    )

    @field_validator("links", mode="before")
    @classmethod
    def _parse_links(cls, v):
        return parse_nested_page(v, FetchLinks)
