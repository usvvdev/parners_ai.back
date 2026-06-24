from sqlalchemy.orm import (
    declared_attr,
    relationship,
)


class PartnerRelationMixin:
    @declared_attr
    def links(cls):
        return relationship(
            "Links",
            secondary="partner_links",
            back_populates="partners",
        )

    @declared_attr
    def utm_source(cls):
        return relationship(
            "UtmSources",
            lazy="selectin",
        )
