# packages

from re import sub

from typing import TypeVar

from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)

# application dependencies

from libs.core.constants import (
    SNAKE_CASE_PATTERN,
    SNAKE_CASE_REPLACEMENT,
)

from libs.core.config import TApplicationConfig

from libs.domain.types._types.options import ConnectionOptions


class ETableModel:
    __name__: str

    @declared_attr.directive
    def __tablename__(cls) -> str:
        table_name = sub(
            SNAKE_CASE_PATTERN,
            SNAKE_CASE_REPLACEMENT,
            cls.__name__,
        )
        return table_name.lower()


class BaseMySQLModel(
    DeclarativeBase,
    ETableModel,
):
    pass


class BaseClickhouseModel(
    DeclarativeBase,
    ETableModel,
):
    pass


TTable = TypeVar(
    "TTable",
    bound=ETableModel,
)


class BaseEngine:
    def __init__(
        self,
        *,
        name: str,
        config: type[TApplicationConfig],
    ) -> None:
        self._name = name
        self._config = config

    @property
    def options(self) -> ConnectionOptions:
        return self._config.engine_options.root.get(
            self._name,
        )
