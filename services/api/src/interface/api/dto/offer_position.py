# packages

from typing import Optional

from pydantic import Field

from datetime import datetime

from fastapi_filters import (
    FilterField,
    FilterSet,
)

# application dependencies

from libs.domain.types._types.common import BaseModelType


class OfferPositionIdentity(BaseModelType):
    wmid: Optional[str] = Field(
        default=None,
        description="ID вебмастера",
    )

    utm_source: Optional[str] = Field(
        default=None,
        description="Сеть с которой работает вебмастер",
    )

    offer: Optional[str] = Field(
        default=None,
        description="Название оффера",
    )


class BaseOfferPositionFields(BaseModelType):
    vitrina: str = Field(
        ...,
        description="Ссылка на витирину партнера",
    )

    position: Optional[int] = Field(
        default=None,
        description="Позиция оффера на витрине",
    )


class FetchOfferPosition(
    BaseOfferPositionFields,
    OfferPositionIdentity,
):
    pass


class InsertOfferPosition(
    BaseOfferPositionFields,
    OfferPositionIdentity,
):
    created_at: datetime = Field(
        default=datetime.now(),
        description="Вермя создания записи",
    )


class FiltersOfferPosition(FilterSet):
    wmid: FilterField[str]

    utm_source: FilterField[str]

    offer: FilterField[str]
