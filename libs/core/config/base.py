# packages

from os import getenv

from typing import Any, TypeVar

from pydantic import Field

from pathlib import PosixPath

from logging import INFO

from pydantic_settings import (
    BaseSettings,
    InitSettingsSource,
    PydanticBaseSettingsSource,
    JsonConfigSettingsSource,
)

# application dependencies

from .mixins import ApplicationOptionsMixin

from libs.domain.utils import get_service_files

from libs.domain.types.enums.config import AppMode

from libs.domain.types._types.common import BaseConfigType


class ApplicationBaseConfig(
    BaseConfigType,
    ApplicationOptionsMixin,
):
    # Application settings
    service_dir: PosixPath = Field(
        ...,
        description="Directory for the application's service files.",
        exclude=True,
    )

    mode: AppMode = Field(
        ...,
        description="Application running mode.",
        exclude=True,
    )

    # Logging level/loggers settings
    logging_level: int = Field(
        default=INFO,
        description="Default logging level",
    )

    loggers: tuple[str, ...] = Field(
        default=("uvicorn.asgi", "uvicorn.access"),
        description="Tuple of logger names to configure",
    )

    api_prefix: str = Field(
        default="/api",
        description="",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: InitSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        base_settings: dict[str, str] = init_settings.init_kwargs

        mode: str | AppMode = getenv(
            "MODE",
            AppMode.PRODUCTION,
        )

        service_file_options = get_service_files(
            base_settings,
            settings_cls,
            mode,
        )

        sources: tuple[PydanticBaseSettingsSource, ...] = (
            init_settings,
            env_settings,
            service_file_options.env_source,
            JsonConfigSettingsSource(
                settings_cls,
                service_file_options.json_file,
            ),
            file_secret_settings,
        )

        return tuple(
            filter(
                None,
                map(lambda x: x, sources),
            )
        )

    @property
    def openai(
        self,
    ) -> dict[str, Any]:
        return self.openai_options.model_dump()


TApplicationConfig = TypeVar(
    "TApplicationConfig",
    bound=ApplicationBaseConfig,
)
