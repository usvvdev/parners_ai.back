from typing import (
    Any,
    Protocol,
    Iterable,
)


class IBaseSQLProtocol(Protocol):
    def fetch_one(
        self,
        id: int,
    ) -> None: ...

    def fetch_many(
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
