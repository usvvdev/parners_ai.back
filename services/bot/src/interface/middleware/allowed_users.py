from aiogram import BaseMiddleware

from aiogram.types import TelegramObject

from libs.domain.types._types.options import TelegramOptions


class AuthMiddleware(BaseMiddleware):
    def __init__(
        self,
        telegram_options: TelegramOptions,
    ):
        self.telegram_options = telegram_options

    async def __call__(
        self,
        handler,
        event: TelegramObject,
        data: dict,
    ):
        user = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        if not self.telegram_options.allowed_users.contains(user.id):
            await data["bot"].send_message(
                chat_id=user.id,
                text="⛔ У вас нет доступа к этому боту.",
            )
            return

        return await handler(event, data)
