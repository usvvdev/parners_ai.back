from pydantic import Field

from typing import Optional

from .offer import FetchOffer

from libs.domain.types._types.common import BaseModelType


class BasePartner(BaseModelType):
    title: str = Field(
        ...,
        description="Название оффера",
    )

    link: str = Field(
        ...,
        description="Ссылка на платформу парнтера",
    )

    is_tracking: bool = Field(
        default=True,
        description="Активность оффера",
    )


class FetchPartner(BasePartner):
    id: int = Field(
        ...,
        description="ID оффера",
    )

    offers: Optional[list[FetchOffer]] = Field(
        default=list,
        description="Офферы, относящиеся к партнеру",
    )


class InsertPartner(BasePartner):
    pass
