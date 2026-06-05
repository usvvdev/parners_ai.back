# packages

from sqlalchemy import (
    Integer,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy.dialects.mysql import TINYINT

# application dependencies

from ..mixins.common import LinkMixin


class PartnerLinkOffer(LinkMixin):
    partner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "partners.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

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

    is_actve: Mapped[bool] = mapped_column(
        TINYINT,
        default=1,
    )
