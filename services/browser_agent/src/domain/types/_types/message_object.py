# packages

from typing import (
    Union,
    Annotated,
)

from pydantic import Field

# application depencies

from libs.domain.types._types.common import BaseModelType


class TextPart(BaseModelType):
    type: str = Field(
        default="text",
        description="",
    )

    text: str = Field(
        ...,
        description="",
    )


class ImageURLObject(BaseModelType):
    url: str = Field(
        ...,
        description="",
    )


class ImageURLPart(BaseModelType):
    type: str = Field(
        default="image_url",
        description="",
    )

    image_url: ImageURLObject = Field(
        ...,
        description="",
    )


ContentPart = Annotated[
    Union[TextPart, ImageURLPart],
    Field(discriminator="type"),
]
