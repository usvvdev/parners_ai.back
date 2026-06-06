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
    pass


class InsertOffer(BaseOffer):
    pass
