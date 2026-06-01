from sqlalchemy.orm import (
    declared_attr,
    relationship,
)


class PartnerRelationMixin:
    @declared_attr
    def links(cls):
        return relationship(
            "Links",
            secondary="partner_link",
            back_populates="partners",
        )
