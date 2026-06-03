# packages

# application dependencies

from ..base import ApplicationBaseConfig

from libs.domain.types.enums.config import AppMode


class ApplicationDevelopmentConfig(ApplicationBaseConfig):
    mode: AppMode = AppMode.DEVELOPMENT
