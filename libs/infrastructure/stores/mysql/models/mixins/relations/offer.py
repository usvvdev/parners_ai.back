from sqlalchemy.orm import (
    declared_attr,
    relationship,
)


class OfferRelationMixin:
    @declared_attr
    def partners(cls):
        return relationship(
            "Partners",
            secondary="partner_offer",
            back_populates="offers",
        )
