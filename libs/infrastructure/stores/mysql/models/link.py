# packages

from sqlalchemy import String

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy.dialects.mysql import (
    TINYINT,
)

# application dependencies

from ...common.sql.models import (
    BaseModel,
    TimestampModel,
)

from .mixins.relations import (
    LinkRelationMixin,
)


class Links(
    BaseModel,
    TimestampModel,
    LinkRelationMixin,
):
    link: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        TINYINT,
        default=True,
        nullable=False,
    )

    __updated_at__: bool = True
