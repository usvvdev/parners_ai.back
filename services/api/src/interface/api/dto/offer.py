from pydantic import Field

from libs.domain.types._types.common import BaseModelType


class BaseOffer(BaseModelType):
    title: str = Field(
        ...,
        description="Название оффера",
    )

    is_active: bool = Field(
        default=True,
        description="Активность оффера",
    )


class FetchOffer(BaseOffer):
    id: int = Field(
        ...,
        description="ID оффера",
    )


class InsertOffer(BaseOffer):
    pass
