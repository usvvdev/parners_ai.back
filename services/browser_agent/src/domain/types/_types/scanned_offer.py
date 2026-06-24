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

    final_url: str = Field(
        default="",
        description="Финальный URL после редиректа",
    )

    wmid: str = Field(
        default="",
        description="wmid партнёра из финального URL",
    )

    utm_source: str = Field(
        default="",
        description="utm_source из финального URL",
    )

    offer_name: str = Field(
        default="",
        description="Извлечённое имя оффера из карточки (до матчинга)",
    )

    match_score: float = Field(
        default=0.0,
        description="Оценка сходства при матчинге (0–100)",
    )
