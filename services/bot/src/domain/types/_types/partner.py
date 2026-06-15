# packages

from typing import Optional

from pydantic import (
    Field,
    field_validator,
)

# application depencies

from .base import (
    BaseFetch,
    PaginatedResponse,
    parse_nested_page,
)

from .link import FetchLinks

from libs.domain.types._types.common import BaseModelType


class BasePartnerFields(BaseModelType):
    is_tracking: bool = Field(
        default=True,
        description="Статус трекинга",
    )

    is_selected: bool = Field(
        default=False,
        description="Избранный партнер",
    )


class PartnerIdentity(BaseModelType):
    wmid: str = Field(
        ...,
        description="WMID вебмастера",
    )


class FetchPartner(
    PartnerIdentity,
    BasePartnerFields,
    BaseFetch,
):
    utm_source: str = Field(
        default="",
        description="UTM-источник партнера",
    )


class FetchPartners(FetchPartner):
    links: PaginatedResponse[FetchLinks] = Field(
        default_factory=lambda: PaginatedResponse(
            items=[],
            total=0,
            page=1,
            size=0,
            pages=0,
        ),
        description="Витрина партнера",
    )

    @field_validator("links", mode="before")
    @classmethod
    def _parse_links(cls, v: PaginatedResponse[FetchLinks] | dict | None):
        return parse_nested_page(v, FetchLinks)


class InsertPartner(
    BasePartnerFields,
):
    wmid: str = Field(
        ...,
        description="WMID вебмастера",
    )

    utm_source_id: int = Field(
        ...,
        description="ID UTM-источника",
    )

    link_ids: list[int] = Field(
        default_factory=list,
        description="ID ссылок партнера",
    )


class UpdatePartner(BasePartnerFields):
    link_ids: Optional[list[int]] = Field(
        default=None,
        description="ID ссылок партнера",
    )
