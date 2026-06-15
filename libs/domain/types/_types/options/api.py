# packages

from typing import Optional

from pydantic import (
    Field,
    computed_field,
)

# application dependencies

from ..common import BaseModelType


class APIOptions(BaseModelType):
    host: Optional[str] = Field(
        default="api",
        description="API host",
        exclude=True,
    )

    port: Optional[int] = Field(
        default=None,
        description="API port",
        exclude=True,
    )

    prefix: Optional[str] = Field(
        default="/api",
        description="API prefix",
        exclude=True,
    )

    @computed_field
    @property
    def base_url(self) -> str:
        port = f":{self.port} " if self.port else ""
        return f"https://{self.host}{port}{self.prefix}"
