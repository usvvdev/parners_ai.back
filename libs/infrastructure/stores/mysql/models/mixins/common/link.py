# packages

from sqlalchemy import Index

from sqlalchemy.orm import declared_attr

# application dependencies

from .....common.base import ETableModel


class LinkMixin(ETableModel):
    __abstract__ = True

    @declared_attr
    def __table_args__(cls) -> tuple[Index]:
        return (
            Index(
                f"idx_{cls.__tablename__}_unique",
                *cls.__annotations__.keys(),
                unique=True,
            ),
        )
