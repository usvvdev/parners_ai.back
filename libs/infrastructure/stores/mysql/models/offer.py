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

from .mixins.relations import (
    OfferRelationMixin,
)

from ...common.sql.models import BaseModel


class Offers(
    BaseModel,
    OfferRelationMixin,
):
    title: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    symbol: Mapped[str] = mapped_column(
        String(8),
        server_default="",
        nullable=False,
    )

    __table_args__ = (
        # fast search
        Index("ix_offers_title", "title"),
    )
