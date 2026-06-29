# packages

from typing import Optional

from pydantic import (
    Field,
    field_validator,
)

from fastapi_filters import (
    FilterField,
    FilterSet,
)

from urllib.parse import (
    urlsplit,
    urlunsplit,
)

from datetime import datetime

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

    @field_validator("link", mode="before")
    @classmethod
    def strip_query_params(cls, v: str) -> str:
        if not isinstance(v, str):
            return v

        parts = urlsplit(v)
        cleaned = parts._replace(query="", fragment="")
        return urlunsplit(cleaned)


class BaseLinkFields(BaseModelType):
    is_active: bool = Field(
        default=True,
        description="Активность оффера",
    )


class FetchLinks(
    LinkIdentity,
    BaseLinkFields,
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

    updated_at: datetime = Field(
        default=datetime.now(),
        description="Текущее время обновления",
    )


class FiltersLink(FilterSet):
    is_active: FilterField[bool]
