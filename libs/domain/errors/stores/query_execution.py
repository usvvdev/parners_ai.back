from .repository import RepositoryException


class QueryExecutionException(RepositoryException):
    def __init__(
        self,
        table: str,
    ) -> None:
        detail = f"Failed to execute query for table '{table}'"

        super().__init__(
            detail=detail,
        )
