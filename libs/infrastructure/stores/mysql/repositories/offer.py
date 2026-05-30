# packages

# application dependencies

from ..models import Offers

from ..repository import MySQLRepository


class OfferRepository(MySQLRepository[Offers]):
    _table: type[Offers] = Offers

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
