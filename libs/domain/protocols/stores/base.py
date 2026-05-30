from typing import (
    Any,
    Protocol,
    Iterable,
)


class IBaseSQLProtocol(Protocol):
    def fetch(
        self,
    ) -> None: ...

    def insert(
        self,
        data: Iterable[Any],
    ) -> None: ...

    def delete(
        self,
        id: int,
    ) -> None: ...
