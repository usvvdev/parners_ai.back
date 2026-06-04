# packages

from typing import Optional

from pydantic import Field

# application dependencies

from .base import BaseFetch

from .offer import FetchOffers

from libs.domain.types._types.common import BaseModelType


class BaseLink(BaseModelType):
    link: str = Field(
        ...,
        description="Название оффера",
    )


class FetchLinks(
    BaseLink,
    BaseFetch,
):
    pass


class FetchLink(
    BaseLink,
    BaseFetch,
):
    is_active: bool = Field(
        default=True,
        description="Активность оффера",
    )

    offers: Optional[list[FetchOffers]] = Field(
        default=None,
        description="Список офферов, связанных с данной ссылкой",
    )


class InsertLink(BaseLink):
    is_active: bool = Field(
        default=True,
        description="Активность оффера",
    )

    offer_ids: Optional[list[int]] = Field(
        default=list,
        description="ID офферов, относящихся к партнеру",
    )
