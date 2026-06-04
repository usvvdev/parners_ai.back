# packages

from pydantic import Field

# application dependencies

from .base import BaseFetch

from libs.domain.types._types.common import BaseModelType


class BaseOffer(BaseModelType):
    title: str = Field(
        ...,
        description="Название оффера",
    )


class FetchOffers(
    BaseOffer,
    BaseFetch,
):
    pass


class FetchOffer(
    BaseOffer,
    BaseFetch,
):
    is_active: bool = Field(
        default=True,
        description="Активность оффера",
    )


class InsertOffer(BaseOffer):
    is_active: bool = Field(
        default=True,
        description="Активность оффера",
    )
