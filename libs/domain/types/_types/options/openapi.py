# packages

from pydantic import (
    Field,
    computed_field,
)

# application dependencies

from ..common import BaseConfigType


class OpenAPIOptions(BaseConfigType):
    debug: bool = Field(
        default=False,
        description="Enable debug mode for OpenAPI.",
    )

    docs_url: str = Field(
        default="/docs",
        description="URL path to the Swagger UI documentation",
    )

    openapi_url: str = Field(
        default="/openapi.json",
        description="URL path to the OpenAPI JSON schema.",
    )

    version: str = Field(
        default="0.0.1",
        description="Application API version.",
    )

    title: str = Field(
        default="API",
        description="Title of the API (shown in docs).",
    )

    @computed_field
    @property
    def root_path(
        self,
    ) -> str:
        if self.title is not None:
            return f"/{self.title}"
        raise ValueError("Application title is not filled")
