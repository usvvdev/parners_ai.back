from .repository import RepositoryException


class ObjectNotFoundException(RepositoryException):
    status_code = 404

    def __init__(
        self,
        table: str,
        id: int | None = None,
    ) -> None:
        detail = (
            f"Object with id={id} not found in table '{table}'"
            if id is not None
            else f"No objects found in table '{table}'"
        )

        super().__init__(
            detail=detail,
        )
