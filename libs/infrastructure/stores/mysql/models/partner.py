# packages

from sqlalchemy import (
    String,
    Index,
    Integer,
    ForeignKey,
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

    utm_source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "utm_sources.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
        nullable=False,
    )

    is_selected: Mapped[bool] = mapped_column(
        TINYINT,
        default=False,
        server_default="0",
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
