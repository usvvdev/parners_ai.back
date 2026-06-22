# packages

from pydantic import Field

# application depencies

from libs.domain.types._types.common import BaseModelType

from libs.domain.types._types.shared import BaseFetchType


class OfferIdentity(BaseModelType):
    title: str = Field(
        ...,
        description="Название оффера",
    )

    symbol: str = Field(
        default="",
        description="Символ оффера",
    )


class FetchOffer(
    OfferIdentity,
    BaseFetchType,
):
    pass


class FetchOffers(FetchOffer):
    pass


class InsertOffer(OfferIdentity):
    pass


class UpdateOffer(OfferIdentity):
    pass
