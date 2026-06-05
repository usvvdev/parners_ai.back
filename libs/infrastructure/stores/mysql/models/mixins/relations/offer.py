from sqlalchemy.orm import (
    declared_attr,
    relationship,
)


class OfferRelationMixin:
    @declared_attr
    def links(cls):
        return relationship(
            "Links",
            secondary="partner_link_offer",
            back_populates="offers",
        )
