from .development import ApplicationDevelopmentConfig

from .production import ApplicationProductionConfig

from .staging import ApplicationStagingConfig

from libs.domain.types.enums.config import AppMode


application_config_mapping: dict[AppMode, type] = {
    AppMode.DEVELOPMENT: ApplicationDevelopmentConfig,
    AppMode.PRODUCTION: ApplicationProductionConfig,
    AppMode.STAGING: ApplicationStagingConfig,
}

__all__: list[str] = [
    "application_config_mapping",
]
