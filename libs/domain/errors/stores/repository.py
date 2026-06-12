from ..base import BaseApplicationException


class RepositoryException(BaseApplicationException):
    status_code = 500

    def __init__(
        self,
        detail: str = "Repository operation failed",
    ) -> None:
        super().__init__(detail=detail)
