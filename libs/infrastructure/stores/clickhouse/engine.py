# application dependencies

from ..common import BaseSQLEngine

from libs.core.config import TApplicationConfig

from libs.domain.types.enums.stores import EngineType


class ClickHouseEngine(BaseSQLEngine):
    _name: str = EngineType.CLICKHOUSE
    _supports_transactions: bool = False

    def __init__(
        self,
        *,
        config: type[TApplicationConfig],
    ) -> None:
        super().__init__(
            name=self._name,
            config=config,
        )
