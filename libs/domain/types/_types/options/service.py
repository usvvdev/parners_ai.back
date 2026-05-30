# coding utf-8

# packages

from typing import (
    Any,
    Optional,
)

from pydantic import Field

from pathlib import PosixPath

# application dependencies

from ..common import BaseModelType


class ServiceFileOptions(BaseModelType):
    env_source: Optional[Any] = Field(
        default=None,
        description="Path to the .env file containing environment variables",
    )

    json_file: Optional[PosixPath] = Field(
        default=None,
        description="Path to the JSON file containing configuration variables",
    )
