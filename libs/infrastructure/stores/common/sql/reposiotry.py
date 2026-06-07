# packages

from typing import Generic

# application dependencies

from ..base import TTable

from .engine import BaseSQLEngine

from .executor import BaseSQLExecutor


class BaseSQLRepository(
    BaseSQLExecutor,
    Generic[TTable],
):
    def __init__(
        self,
        *,
        engine: BaseSQLEngine,
        table: type[TTable],
    ) -> None:
        super().__init__(
            engine=engine,
        )
        self._table = table
