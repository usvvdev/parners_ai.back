from typing import Protocol

from .base import IBaseSQLProtocol


class IClickhouseProtocol(IBaseSQLProtocol, Protocol):
    pass
