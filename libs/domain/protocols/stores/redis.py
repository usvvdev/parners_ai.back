from typing import (
    Any,
    Protocol,
    Iterable,
)


class IRedisProtocol(Protocol):
    def get(
        self,
        key: str,
    ) -> None: ...

    def set(
        self,
        key: str,
        value: Iterable[Any] | Any,
        expire: int | None = None,
    ) -> None: ...

    def delete(
        self,
        key: str,
    ) -> None: ...
