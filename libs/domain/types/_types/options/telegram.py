# packages

from typing import Optional

from pydantic import (
    Field,
    computed_field,
)

# application depencies

from ..common import BaseModelType


class APIOptions(BaseModelType):
    host: Optional[str] = Field(
        default="api",
        description="API хост(имя сервиса)",
        exclude=True,
    )

    port: Optional[int] = Field(
        default=8000,
        description="API порт",
        exclude=True,
    )

    prefix: Optional[str] = Field(
        default="/api",
        description="API префикс(базовый uri)",
        exclude=True,
    )

    @computed_field
    @property
    def base_url(self) -> str:
        return f"https://{self.host}:{self.port}{self.prefix}"


class TelegramOptions(BaseModelType):
    bot_token: Optional[str] = Field(
        default=None,
        description="Телеграмм бот API ключ",
        exclude=True,
    )

    api: APIOptions = Field(
        default_factory=APIOptions,
        exclude=True,
    )

    @computed_field
    @property
    def api_base_url(self) -> str:
        return self.api.base_url
