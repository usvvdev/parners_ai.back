from sqlalchemy.orm import (
    declared_attr,
    relationship,
)


class LinkRelationMixin:
    @declared_attr
    def partners(cls):
        return relationship(
            "Partners",
            secondary="partner_link",
            back_populates="links",
        )
