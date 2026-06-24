# packages

from sqlalchemy import Integer

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

# application dependencies

from ...base import BaseMySQLModel


class BaseModel(BaseMySQLModel):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
