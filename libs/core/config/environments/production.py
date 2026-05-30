from ..base import ApplicationBaseConfig

from libs.domain.types.enums.config import AppMode


class ApplicationProductionConfig(ApplicationBaseConfig):
    mode: AppMode = AppMode.PRODUCTION
