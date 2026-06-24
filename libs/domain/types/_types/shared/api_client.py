# packages

from typing import Any

from pydantic import (
    Field,
    ConfigDict,
)

# application dependencies

from ..common import BaseModelType


class APIClients(BaseModelType):
    client: Any = Field(
        ...,
        description="",
    )

    # api clients
    model_config = ConfigDict(
        extra="allow",
    )

    async def close(self) -> None:
        await self.client.aclose()
