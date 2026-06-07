# packages

from typing import Generic

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

# application dependencies

from ..common import (
    TTable,
    BaseSQLRepository,
)

from .engine import MySQLEngine

from libs.domain.protocols.stores import IMySQLProtocol


class MySQLRepository(
    BaseSQLRepository,
    IMySQLProtocol,
    Generic[TTable],
):
    def __init__(
        self,
        *,
        engine: MySQLEngine,
        table: type[TTable],
    ) -> None:
        super().__init__(
            engine=engine,
            table=table,
        )
