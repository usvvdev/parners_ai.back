# packages

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

# application dependencies

from .base import BasePydanticModel


class BaseConfigType(
    BaseSettings,
    BasePydanticModel,
):
    model_config = SettingsConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        extra="allow",
        env_file=None,
        env_nested_delimiter="__",
    )
