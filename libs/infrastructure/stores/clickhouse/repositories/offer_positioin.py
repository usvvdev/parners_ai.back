# packages

# application dependencies

from ..models import OfferPositions

from ..repository import ClickHouseRepository


class OfferPositionRepository(ClickHouseRepository[OfferPositions]):
    _table: type[OfferPositions] = OfferPositions

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
