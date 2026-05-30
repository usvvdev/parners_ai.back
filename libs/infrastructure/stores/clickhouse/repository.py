# packages

from typing import Generic

# application dependencies

from ..common import (
    TTable,
    BaseSQLRepository,
)

from .engine import ClickHouseEngine

from libs.domain.protocols.stores import IClickhouseProtocol


class ClickHouseRepository(
    BaseSQLRepository,
    IClickhouseProtocol,
    Generic[TTable],
):
    def __init__(
        self,
        *,
        engine: ClickHouseEngine,
        table: type[TTable],
    ) -> None:
        super().__init__(
            engine=engine,
            table=table,
        )
