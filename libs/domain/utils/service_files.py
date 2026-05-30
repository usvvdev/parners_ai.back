# packages

from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
)

# application dependencies

from libs.domain.types.enums.config import AppMode

from ..types._types.options import ServiceFileOptions


def get_service_files(
    base_settings: dict[str, str],
    settings_cls: type[BaseSettings],
    mode: AppMode,
) -> ServiceFileOptions:
    service_dir_raw = base_settings.get("service_dir")

    if not service_dir_raw:
        raise ValueError("Service directory must be provided")

    service_dir = Path(service_dir_raw)

    if not service_dir.exists():
        raise ValueError(f"Service directory does not exist: {service_dir}")

    config_file = service_dir / f"{mode}.config.json"
    env_file = service_dir / ".env"

    env_source = DotEnvSettingsSource(
        settings_cls,
        env_file=env_file if env_file.exists() else None,
    )

    return ServiceFileOptions(
        env_source=env_source,
        json_file=config_file,
    )
