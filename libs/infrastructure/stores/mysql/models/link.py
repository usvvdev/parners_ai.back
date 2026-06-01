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
    LinkRelationMixin,
)


class Links(
    BaseMixin,
    TimestampMixin,
    LinkRelationMixin,
):
    link: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        TINYINT,
        default=True,
        nullable=False,
    )

    __updated_at__: bool = True

    __table_args__ = (
        # fast search
        Index("ix_offers_link", "link"),
    )
