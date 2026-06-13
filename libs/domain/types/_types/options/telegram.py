# packages

from typing import Optional

from pydantic import (
    RootModel,
    Field,
    computed_field,
)

# application depencies

from ..common import BaseModelType

from ...enums.config import UserRole


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
        return f"http://{self.host}:{self.port}{self.prefix}"


class UserOptions(BaseModelType):
    role: UserRole = Field(
        default="",
        description="Роль пользователя",
    )

    notifications: bool = Field(
        default=True,
        description="Отправлять ли нотификации",
    )


class AllowedUsers(RootModel[dict[str, UserOptions]]):
    def contains(
        self,
        user_id: int,
    ) -> bool:
        return str(user_id) in self.root

    def get(
        self,
        user_id: int,
    ) -> UserOptions | None:
        return self.root.get(str(user_id))

    @property
    def ids(self) -> set[int]:
        return {int(user_id) for user_id in self.root}


class TelegramOptions(BaseModelType):
    bot_token: Optional[str] = Field(
        default=None,
        description="Телеграмм бот API ключ",
        exclude=True,
    )

    api_optins: APIOptions = Field(
        default_factory=APIOptions,
        exclude=True,
    )

    allowed_users: AllowedUsers = Field(
        default_factory=AllowedUsers,
        description="Авторизованные айди пользователей",
    )

    @computed_field
    @property
    def api_base_url(self) -> str:
        return self.api_optins.base_url
