# packages


from sqlalchemy import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from datetime import datetime

from clickhouse_sqlalchemy.types import (
    String,
    DateTime,
    Int16,
)


# application dependencies

from ...common.base import BaseClickhouseModel


class OfferPositions(BaseClickhouseModel):
    wmid: Mapped[str] = mapped_column(
        String(length=128),
        nullable=False,
    )

    utm_source: Mapped[str] = mapped_column(
        String(length=64),
        nullable=False,
    )

    vitrina: Mapped[str] = mapped_column(
        String(length=2048),
        nullable=False,
    )

    offer: Mapped[str] = mapped_column(
        String(length=128),
        nullable=False,
    )

    position: Mapped[int] = mapped_column(
        Int16,
        server_default="null",
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        primary_key=True,
        server_default=func.now(),
    )
