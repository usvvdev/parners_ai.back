# packages

from pydantic import Field

# application depencies

from .base import BaseFetch

from libs.domain.types._types.common import BaseModelType


class OfferIdentity(BaseModelType):
    title: str = Field(
        ...,
        description="Название оффера",
    )


class FetchOffer(
    OfferIdentity,
    BaseFetch,
):
    pass


class InsertOffer(OfferIdentity):
    pass


class UpdateOffer(OfferIdentity):
    pass
