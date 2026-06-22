# packages

from pydantic import Field

# application depencies

from .scanned_offer import ScannedOffer

from libs.domain.types._types.common import BaseModelType


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
