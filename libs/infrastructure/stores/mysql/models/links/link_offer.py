# packages

from sqlalchemy import (
    Integer,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

# application dependencies

from ..mixins.common import LinkMixin


class LinkOffer(LinkMixin):
    link_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "links.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    offer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "offers.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
