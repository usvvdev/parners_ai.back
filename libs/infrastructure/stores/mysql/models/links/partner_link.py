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

from ....common.sql.models import LinkModel


class PartnerLinks(LinkModel):
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
