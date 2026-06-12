# packages

from typing import Optional

from pydantic import Field, field_validator

from fastapi_pagination import Page

# application dependencies

from .base import BaseFetch

from .offer import FetchOffers

from libs.domain.types._types.common import BaseModelType


class LinkIdentity(BaseModelType):
    link: str = Field(
        ...,
        description="Название оффера",
    )


class BaseLinkFields(BaseModelType):
    is_active: bool = Field(
        default=True,
        description="Активность оффера",
    )


class FetchLinks(
    LinkIdentity,
    BaseFetch,
):
    offers: Optional[list[FetchOffers | str]] = Field(
        default=None,
        description="Список офферов, связанных с данной ссылкой",
    )

    @field_validator("offers", mode="after")
    def validate_offers(
        cls,
        value: Optional[list[FetchOffers]],
    ) -> list[str] | None:
        if value is not None:
            return [item.symbol for item in value]
        return value


class FetchLink(
    LinkIdentity,
    BaseLinkFields,
    BaseFetch,
):
    offers: Optional[Page[FetchOffers]] = Field(
        default=None,
        description="Список офферов, связанных с данной ссылкой",
    )


class InsertLink(
    LinkIdentity,
    BaseLinkFields,
):
    offer_ids: list[int] = Field(
        default_factory=list,
        description="ID офферов, относящихся к партнеру",
    )


class UpdateLink(BaseLinkFields):
    offer_ids: Optional[list[int]] = Field(
        default=None,
        description="ID офферов, относящихся к партнеру",
    )
