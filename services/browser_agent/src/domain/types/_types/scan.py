# packages

from pydantic import Field

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
        description="URL перехода с карточки оффера",
    )


class PartnerResult(BaseModelType):
    link: str = Field(
        default="",
        description="URL проанализированной витрины",
    )

    total_cards: int = Field(
        default=0,
        description="Общее количество карточек",
    )

    target_offers_found: list[ScannedOffer] = Field(
        default_factory=list,
        description="Найденные целевые офферы",
    )
