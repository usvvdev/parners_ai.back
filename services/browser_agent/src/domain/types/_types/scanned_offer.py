# packages

from pydantic import Field

# application depencies

from libs.domain.types._types.common import BaseModelType


class ScannedOffer(BaseModelType):
    title: str = Field(
        default="",
        description="Название оффера",
    )

    position: int = Field(
        default=0,
        description="Позиция на странице",
    )

    is_found: bool = Field(
        default=False,
        description="Найден ли оффер на странице",
    )

    url: str = Field(
        default="",
        description=(
            "Промежуточный href с карточки оффера на витрине "
            "(до редиректа; wmid/utm_source могут отсутствовать)"
        ),
    )
