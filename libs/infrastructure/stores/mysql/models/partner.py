# packages

from sqlalchemy import (
    String,
    Index,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy.dialects.mysql import (
    TINYINT,
)

# application dependencies

from ...common.sql.models import (
    BaseModel,
    TimestampModel,
)

from .mixins.relations import PartnerRelationMixin


class Partners(
    BaseModel,
    TimestampModel,
    PartnerRelationMixin,
):
    wmid: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    utm_source: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    is_tracking: Mapped[bool] = mapped_column(
        TINYINT,
        default=True,
        nullable=False,
    )

    __updated_at__: bool = True

    __table_args__ = (
        # fast search
        Index("ix_partner_wmid", "wmid"),
    )
