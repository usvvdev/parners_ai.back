# packages

from pydantic import (
    Field,
    field_validator,
)

from typing import Optional

# application depencies

from .offer import FetchOffer

from libs.domain.types._types.shared import (
    BaseFetchType,
    PaginatedResponse,
)

from libs.domain.utils import parse_paginated_response

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
    BaseLinkFields,
    BaseFetchType,
):
    offers: list[str] = Field(
        default_factory=list,
        description="Символы офферов ссылки",
    )

    @field_validator(
        "offers",
        mode="before",
    )
    @classmethod
    def validate_offers(
        cls,
        value: Optional[list],
    ) -> list:
        return value if value is not None else []


class FetchLink(
    LinkIdentity,
    BaseLinkFields,
    BaseFetchType,
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

    @field_validator(
        "offers",
        mode="before",
    )
    @classmethod
    def validate_offers(
        cls,
        value: Optional[PaginatedResponse[FetchOffer] | dict],
    ) -> PaginatedResponse[FetchOffer]:
        return parse_paginated_response(
            value,
            FetchOffer,
        )


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
