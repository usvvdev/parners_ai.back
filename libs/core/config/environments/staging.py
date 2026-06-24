# packages

# application dependencies

from ..base import ApplicationBaseConfig

from libs.domain.types.enums.config import AppMode


class ApplicationStagingConfig(ApplicationBaseConfig):
    mode: AppMode = AppMode.STAGING
