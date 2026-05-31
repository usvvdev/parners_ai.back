# packages

from typing import Optional

from pydantic import (
    RootModel,
    SecretStr,
    ConfigDict,
    Field,
    computed_field,
)

from urllib.parse import quote_plus

# application dependencies

from ..common import BaseModelType

from ...enums.stores import EngineType

from libs.core.constants import (
    URL_REQUIRED_FIELDS,
    URL_TEMPLATE,
)


class DSNOptions(BaseModelType):
    driver: Optional[str] = Field(
        default=None,
        description="Connection driver (e.g., 'asyncpg' for PostgreSQL)",
        exclude=True,
    )

    username: Optional[str] = Field(
        default=None,
        description="Connection username",
        exclude=True,
    )

    password: Optional[SecretStr] = Field(
        default=None,
        description="Connection password",
        exclude=True,
    )

    host: Optional[str] = Field(
        default="localhost",
        description="Connection host",
        exclude=True,
    )

    port: Optional[int] = Field(
        default=None,
        description="Connection port",
        exclude=True,
    )

    database: Optional[str | int] = Field(
        default=None,
        description="Connection database",
        exclude=True,
    )

    @computed_field
    @property
    def url(
        self,
    ) -> str | None:
        if not all(getattr(self, field) for field in URL_REQUIRED_FIELDS):
            return None

        auth = ":".join(
            quote_plus(v)
            for v in [
                self.username,
                self.password.get_secret_value() if self.password else None,
            ]
            if v
        )

        return URL_TEMPLATE.format(
            driver=self.driver,
            auth=f"{auth}@" if auth else "",
            host=self.host,
            port=self.port,
            db_path=f"/{self.database}" if self.database else "",
        )


class ConnectionOptions(DSNOptions):
    pool_size: Optional[int] = Field(
        default=None,
        description="Base pool size (SQL engines only)",
    )

    max_overflow: Optional[int] = Field(
        default=None,
        description="Overflow pool connections (SQL engines only)",
    )

    echo: Optional[bool] = Field(
        default=None,
        description="Enable SQL debug logging",
    )


class EngineOptions(RootModel[dict[EngineType, ConnectionOptions]]):
    model_config = ConfigDict(
        use_enum_values=True,
    )
