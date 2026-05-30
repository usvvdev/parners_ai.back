# packages

from pydantic import (
    RootModel,
    ConfigDict,
)

# application dependencies

from .base import BasePydanticModel


class BaseRootModelType(
    RootModel,
    BasePydanticModel,
):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        loc_by_alias=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
