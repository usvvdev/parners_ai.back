# packages

from typing import Optional

from pydantic import (
    Field,
    field_validator,
)

# application depencies

from .base import BaseFetch

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
    pass


class FetchLink(
    LinkIdentity,
    BaseLinkFields,
    BaseFetch,
):
    offers: list[FetchOffer] = Field(
        default_factory=list,
        description="Офферы, привязанные к ссылке",
    )

    @field_validator("offers", mode="before")
    @classmethod
    def _normalize_offers(cls, v: list | None) -> list:
        return v if v is not None else []


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
