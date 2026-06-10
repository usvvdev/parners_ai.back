# packages

from aiogram.types import InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application dependencies

from ..callbacks import NavCD


def append_list_pagination(
    builder: InlineKeyboardBuilder,
    *,
    level: str,
    page: int,
    pages: int,
) -> None:
    if pages <= 1:
        return

    buttons: list[InlineKeyboardButton] = []

    if page > 1:
        buttons.append(
            InlineKeyboardButton(
                text="◀️ Назад",
                callback_data=NavCD(level=level, page=page - 1).pack(),
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=f"· {page}/{pages} ·",
            callback_data=NavCD(level=level, page=page).pack(),
        )
    )

    if page < pages:
        buttons.append(
            InlineKeyboardButton(
                text="Вперёд ▶️",
                callback_data=NavCD(level=level, page=page + 1).pack(),
            )
        )

    builder.row(*buttons)
