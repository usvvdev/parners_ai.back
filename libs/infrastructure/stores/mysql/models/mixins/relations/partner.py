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
