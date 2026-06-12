# packages

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application depencies

from ..dto.callback import NavigationCD

from ....domain.types._types.base import PaginatedResponse


def build_list_text(
    result: PaginatedResponse,
    *,
    title: str,
    empty: str,
) -> str:
    if result.total:
        text = f"{title} ({result.total})"
    elif result.items:
        text = f"{title}:"
    else:
        text = empty

    if result.pages > 1:
        text += f"\nСтраница {result.page} из {result.pages}"

    return text


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
                callback_data=NavigationCD(level=level, page=page - 1).pack(),
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=f"· {page}/{pages} ·",
            callback_data=NavigationCD(level=level, page=page).pack(),
        )
    )

    if page < pages:
        buttons.append(
            InlineKeyboardButton(
                text="Вперёд ▶️",
                callback_data=NavigationCD(level=level, page=page + 1).pack(),
            )
        )

    builder.row(*buttons)


def build_form_prompt(
    text: str,
    cancel_data,
) -> tuple[str, InlineKeyboardMarkup]:
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Отмена", callback_data=cancel_data)
    builder.adjust(1)

    return text, builder.as_markup()
