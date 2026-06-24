from sqlalchemy.orm import (
    declared_attr,
    relationship,
)


class OfferRelationMixin:
    @declared_attr
    def links(cls):
        return relationship(
            "Links",
            secondary="link_offers",
            back_populates="offers",
        )
