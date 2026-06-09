# packages

from pydantic import Field, field_validator

# application dependencies

from .offer import OfferSummary

from libs.domain.types._types.common import BaseModelType


class LinkSummary(BaseModelType):
    id: int = Field(
        ...,
        description="ID ссылки",
    )

    link: str = Field(
        ...,
        description="URL витрины партнера",
    )


class LinkDetail(BaseModelType):
    id: int = Field(
        ...,
        description="ID ссылки",
    )

    link: str = Field(
        ...,
        description="URL витрины партнера",
    )

    is_active: bool = Field(
        ...,
        description="Активность ссылки",
    )

    offers: list[OfferSummary] = Field(
        default_factory=list,
        description="Офферы, привязанные к ссылке",
    )

    @field_validator("offers", mode="before")
    @classmethod
    def _normalize_offers(cls, v: list | None) -> list:
        return v if v is not None else []
