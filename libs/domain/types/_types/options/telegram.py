# packages

from typing import Optional

from pydantic import (
    RootModel,
    Field,
    computed_field,
)

# application depencies

from ..common import BaseModelType

from .api import APIOptions

from ...enums.config import UserRole


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


class ChatOptions(BaseModelType):
    group_chat_id: Optional[int] = Field(
        default=None,
        description="Чат для отправки сообщения",
    )

    topic_id: Optional[int] = Field(
        default=None,
        description="Тема для сообщений",
    )


class TelegramOptions(BaseModelType):
    bot_token: Optional[str] = Field(
        default=None,
        description="Телеграмм бот API ключ",
        exclude=True,
    )

    api_options: APIOptions = Field(
        default_factory=APIOptions,
        exclude=True,
    )

    allowed_users: Optional[AllowedUsers] = Field(
        default_factory=lambda: AllowedUsers(root={}),
        description="Авторизованные айди пользователей",
    )

    chat_options: Optional[ChatOptions] = Field(
        default_factory=ChatOptions,
        description="Чат для работы с ботом",
    )

    dashboard_url: Optional[str] = Field(
        default=None,
        description="Ссылка к подключенному дешу",
    )

    @computed_field
    @property
    def api_base_url(self) -> str:
        return self.api_options.base_url
