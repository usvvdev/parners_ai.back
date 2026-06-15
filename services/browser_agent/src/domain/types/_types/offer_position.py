# packages

from typing import Optional

from pydantic import Field

from datetime import datetime

from libs.domain.types._types.common import BaseModelType


class InsertOfferPosition(BaseModelType):
    wmid: Optional[str] = Field(
        default=None,
    )

    utm_source: Optional[str] = Field(
        default=None,
    )

    offer: Optional[str] = Field(
        default=None,
    )

    vitrina: str = Field(
        ...,
        description="URL витрины",
    )

    position: Optional[int] = Field(
        default=None,
    )

    created_at: datetime = Field(
        default=datetime.now(),
    )
