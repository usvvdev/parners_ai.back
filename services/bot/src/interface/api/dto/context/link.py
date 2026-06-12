from typing import Optional

from pydantic import Field

from .....domain.types.enums import OfferPickMode

from libs.domain.types._types.common import BaseModelType


class LinkContext(BaseModelType):
    l_id: int = Field(
        default=0,
        description="",
    )

    p_id: int = Field(
        default=0,
        description="",
    )

    offer_pick_mode: OfferPickMode = Field(
        default=OfferPickMode.CREATE,
        description="",
    )

    selected_offer_ids: list[int] = Field(
        default_factory=list,
        description="",
    )

    link: Optional[str] = Field(
        default=None,
        description="",
    )
