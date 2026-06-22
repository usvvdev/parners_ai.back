# packages

from pydantic import (
    Field,
    ConfigDict,
)

# application dependencies

from ..common.model import BaseModelType


class Params(BaseModelType):
    page: int = Field(
        ...,
        description="",
    )

    size: int = Field(
        ...,
        description="",
    )

    model_config = ConfigDict(
        extra="allow",
    )
