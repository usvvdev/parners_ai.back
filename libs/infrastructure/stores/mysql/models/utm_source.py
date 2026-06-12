# packages

from sqlalchemy import (
    String,
    Index,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

# application dependencies

from ...common.sql.models import BaseModel


class UtmSources(BaseModel):
    title: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    __table_args__ = (
        # fast search
        Index("ix_utm_sources_title", "title"),
    )
