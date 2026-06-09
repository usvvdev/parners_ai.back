# packages

from typing import Optional

from pydantic import Field

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
    pass


class FetchLink(
    LinkIdentity,
    BaseLinkFields,
    BaseFetch,
):
    offers: list[FetchOffers] | None = Field(
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


class UpdateLink(InsertLink):
    pass
