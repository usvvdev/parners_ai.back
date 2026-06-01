from sqlalchemy.orm import (
    declared_attr,
    relationship,
)


class PartnerRelationMixin:
    @declared_attr
    def offers(cls):
        return relationship(
            "Offers",
            secondary="partner_offer",
            back_populates="partners",
        )

    @declared_attr
    def links(cls):
        return relationship(
            "Links",
            secondary="partner_link",
            back_populates="partners",
        )
