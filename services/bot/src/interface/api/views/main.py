# packages

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application depencies

from ..dto.callback import NavigationCD

from ....domain.types.enums.common import NavLevel


class MainView:
    @staticmethod
    def build() -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        builder.button(
            text="📂 Список партнеров",
            callback_data=NavigationCD(level=NavLevel.PARTNERS),
        )
        builder.button(
            text="🔗 Список витрин",
            callback_data=NavigationCD(level=NavLevel.LINKS),
        )
        builder.button(
            text="🎁 Список офферов",
            callback_data=NavigationCD(level=NavLevel.OFFERS),
        )
        builder.adjust(1)

        return (
            "👋 Добро пожаловать в CRM!\nВыберите действие:",
            builder,
        )
