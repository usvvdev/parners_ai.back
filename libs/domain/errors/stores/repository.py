from ..base import BaseApplicationException


class RepositoryException(BaseApplicationException):
    status_code = 500
