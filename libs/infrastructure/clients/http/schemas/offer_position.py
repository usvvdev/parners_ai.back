# packages

from pydantic import Field

from datetime import datetime

from typing import Optional

# application depencies

from libs.domain.types._types.common import BaseModelType


class InsertOfferPosition(BaseModelType):
    wmid: Optional[str] = Field(
        default=None,
        description="",
    )

    utm_source: Optional[str] = Field(
        default=None,
        description="",
    )

    offer: Optional[str] = Field(
        default=None,
        description="",
    )

    vitrina: str = Field(
        ...,
        description="URL витрины",
    )

    position: Optional[int] = Field(
        default=None,
        description="",
    )

    created_at: datetime = Field(
        default=datetime.now(),
        description="",
    )
