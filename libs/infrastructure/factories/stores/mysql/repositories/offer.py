from ..engine import MySQLEngineFactory

from libs.infrastructure.stores.common import TTable

from libs.infrastructure.stores.mysql import MySQLRepository

from libs.infrastructure.stores.mysql.models import Offers


class MySQLOfferRepository:
    @staticmethod
    def create(
        engine: MySQLEngineFactory,
        table: type[TTable] = Offers,
    ) -> MySQLRepository[Offers]:
        return MySQLRepository(
            engine=engine,
            table=table,
        )
