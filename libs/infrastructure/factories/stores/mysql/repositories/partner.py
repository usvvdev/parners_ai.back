from ..engine import MySQLEngineFactory

from libs.infrastructure.stores.common import TTable

from libs.infrastructure.stores.mysql import MySQLRepository

from libs.infrastructure.stores.mysql.models import Partners


class MySQLPartnerRepository:
    @staticmethod
    def create(
        engine: MySQLEngineFactory,
        table: type[TTable] = Partners,
    ) -> MySQLRepository[Partners]:
        return MySQLRepository(
            engine=engine,
            table=table,
        )
