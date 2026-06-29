# packages

from datetime import datetime

from typing import Optional

from pydantic import Field

# application depencies

from libs.domain.types._types.common import BaseModelType


class BaseOfferPosition(BaseModelType):
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


class FetchOfferPosition(BaseOfferPosition):
    created_at: Optional[datetime] = Field(
        default=None,
        description="",
    )


class InsertOfferPosition(BaseOfferPosition):
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="",
    )
