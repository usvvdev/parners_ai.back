# packages

from pydantic import Field

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
