# packages

# application dependencies

from ..models import Partners

from ..repository import MySQLRepository


class PartnerRepository(MySQLRepository[Partners]):
    _table: type[Partners] = Partners

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            table=self._table,
            *args,
            **kwargs,
        )
