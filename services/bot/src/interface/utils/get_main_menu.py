# packages

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application dependencies

from ..callbacks import NavCD


def get_main_menu():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📂 Список партнеров",
        callback_data=NavCD(level="partners"),
    )
    builder.button(
        text="🔗 Список ссылок",
        callback_data=NavCD(level="links"),
    )
    builder.button(
        text="🎁 Список офферов",
        callback_data=NavCD(level="offers"),
    )
    builder.adjust(1)

    return (
        "👋 Добро пожаловать в CRM!\nВыберите действие:",
        builder.as_markup(),
    )
