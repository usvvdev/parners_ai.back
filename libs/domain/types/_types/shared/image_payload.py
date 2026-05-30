# packages

from pydantic import field_validator

# application dependencies

from ..common import BaseModelType


class ImagePayload(BaseModelType):
    value: str

    @field_validator("value", mode="before")
    @classmethod
    def normalize(cls, value: str) -> str:
        if value.startswith("data:image"):
            return value

        return f"data:image/jpeg;base64,{value}"
