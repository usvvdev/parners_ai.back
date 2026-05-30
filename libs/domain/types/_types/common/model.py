# packages

from pydantic import (
    BaseModel,
    ConfigDict,
)

# application dependencies

from .base import BasePydanticModel


class BaseModelType(
    BaseModel,
    BasePydanticModel,
):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        loc_by_alias=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
