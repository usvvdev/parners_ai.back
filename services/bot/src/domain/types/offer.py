# packages

from pydantic import Field

# application dependencies

from libs.domain.types._types.common import BaseModelType


class OfferSummary(BaseModelType):
    id: int = Field(
        ...,
        description="ID оффера",
    )

    title: str = Field(
        ...,
        description="Название оффера",
    )
