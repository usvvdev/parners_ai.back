from sqlalchemy.orm import (
    declared_attr,
    relationship,
)


class UTMSouceRelationMixin:
    @declared_attr
    def partners(cls):
        return relationship(
            "Partners",
            back_populates="utm_source",
        )
