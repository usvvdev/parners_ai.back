# packages

from pydantic import Field

# application depencies

from .offer import Offer

from libs.domain.types._types.common import BaseModelType


class PartnerResult(BaseModelType):
    """Результат парсинга страницы партнера"""

    link: str = Field(
        default="",
        description="URL страницы партнера, которая была проанализирована",
    )

    total_cards: int = Field(
        default=0,
        description="Общее количество найденных карточек на странице",
    )

    target_offers_found: list[Offer] = Field(
        description="Список найденных целевых офферов"
    )
