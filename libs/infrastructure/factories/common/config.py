# application depencies

from os import getenv

from libs.core.config import TApplicationConfig

from libs.core.config.environments import application_config_mapping


class ApplicationConfigFactory:
    @staticmethod
    def create(
        service_dir: str,
    ) -> type[TApplicationConfig]:
        mode = getenv("APP_MODE", "production")

        config_class = application_config_mapping.get(mode)
        if not config_class:
            raise ValueError(f"Invalid application mode: {mode}")

        return config_class(
            service_dir=service_dir,
        )
