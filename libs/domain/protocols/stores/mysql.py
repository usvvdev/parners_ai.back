from typing import (
    Any,
    Protocol,
    Iterable,
)

from .base import IBaseSQLProtocol


class IMySQLProtocol(IBaseSQLProtocol, Protocol):
    def update(
        self,
        id: int,
        data: Iterable[Any],
    ) -> None: ...
