class BaseApplicationException(Exception):
    status_code: int = 500

    def __init__(
        self,
        detail: str,
    ) -> None:
        self.detail = detail

        super().__init__(
            self.status_code,
            detail,
        )
