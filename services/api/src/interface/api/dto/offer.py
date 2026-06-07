# packages

from pydantic import Field

# application dependencies

from .base import BaseFetch

from libs.domain.types._types.common import BaseModelType


class OfferIdentity(BaseModelType):
    title: str = Field(
        ...,
        description="Название оффера",
    )


class FetchOffers(
    OfferIdentity,
    BaseFetch,
):
    pass


class FetchOffer(
    OfferIdentity,
    BaseFetch,
):
    pass


class InsertOffer(OfferIdentity):
    pass


class UpdateOffer(BaseModelType):
    pass
