from typing import Optional

from pydantic import Field

from .offer import FetchOffer

from libs.domain.types._types.common import BaseModelType


class BaseLink(BaseModelType):
    link: str = Field(
        ...,
        description="Название оффера",
    )

    is_active: bool = Field(
        default=True,
        description="Активность оффера",
    )


class FetchLink(BaseLink):
    id: int = Field(
        ...,
        description="ID оффера",
    )


class InsertLink(BaseLink):
    pass
