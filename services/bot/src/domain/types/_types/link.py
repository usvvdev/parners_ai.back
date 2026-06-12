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

from .offer import FetchOffer

from libs.domain.types._types.common import BaseModelType


class LinkIdentity(BaseModelType):
    link: str = Field(
        ...,
        description="URL ссылки",
    )


class BaseLinkFields(BaseModelType):
    is_active: bool = Field(
        default=True,
        description="Активность ссылки",
    )


class FetchLinks(
    LinkIdentity,
    BaseFetch,
):
    offers: list[str] = Field(
        default_factory=list,
        description="Символы офферов ссылки",
    )

    @field_validator("offers", mode="before")
    @classmethod
    def _normalize_offers(cls, v: list | None) -> list:
        return v if v is not None else []


class FetchLink(
    LinkIdentity,
    BaseLinkFields,
    BaseFetch,
):
    offers: PaginatedResponse[FetchOffer] = Field(
        default_factory=lambda: PaginatedResponse(
            items=[],
            total=0,
            page=1,
            size=0,
            pages=0,
        ),
        description="Офферы, привязанные к ссылке",
    )

    @field_validator("offers", mode="before")
    @classmethod
    def _parse_offers(cls, v: PaginatedResponse[FetchOffer] | dict | None):
        return parse_nested_page(v, FetchOffer)


class InsertLink(
    LinkIdentity,
    BaseLinkFields,
):
    offer_ids: list[int] = Field(
        default_factory=list,
        description="ID офферов ссылки",
    )


class UpdateLink(BaseLinkFields):
    link: Optional[str] = Field(
        default=None,
        description="URL ссылки",
    )

    offer_ids: Optional[list[int]] = Field(
        default=None,
        description="ID офферов ссылки",
    )
