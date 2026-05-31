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

from .mixins.common import (
    BaseMixin,
    TimestampMixin,
)

from .mixins.relations import (
    PartnerRelationMixin,
)


class Partners(
    BaseMixin,
    TimestampMixin,
    PartnerRelationMixin,
):
    title: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    link: Mapped[str] = mapped_column(
        String(2048),
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
        Index("ix_partner_title", "title"),
    )
