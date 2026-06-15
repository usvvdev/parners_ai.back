# packages

from aiogram.filters.callback_data import CallbackData

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application depencies

from ..dto.callback import NavigationCD

from ....core.constants import FILTER_ALL

from ....domain.types._types.base import PaginatedResponse

from ....domain.types.enums.common import NavLevel


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
    fa: int = FILTER_ALL,
    ft: int = FILTER_ALL,
    fs: int = FILTER_ALL,
) -> None:
    if pages <= 1:
        return

    buttons: list[InlineKeyboardButton] = []

    if page > 1:
        buttons.append(
            InlineKeyboardButton(
                text="◀",
                callback_data=NavigationCD(
                    level=level,
                    page=page - 1,
                    fa=fa,
                    ft=ft,
                    fs=fs,
                ).pack(),
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=f"{page}/{pages}",
            callback_data=NavigationCD(
                level=level,
                page=page,
                fa=fa,
                ft=ft,
                fs=fs,
            ).pack(),
        )
    )

    if page < pages:
        buttons.append(
            InlineKeyboardButton(
                text="▶",
                callback_data=NavigationCD(
                    level=level,
                    page=page + 1,
                    fa=fa,
                    ft=ft,
                    fs=fs,
                ).pack(),
            )
        )

    builder.row(*buttons)


def append_detail_pagination(
    builder: InlineKeyboardBuilder,
    *,
    page: int,
    pages: int,
    build_callback,
) -> None:
    if pages <= 1:
        return

    buttons: list[InlineKeyboardButton] = []

    if page > 1:
        buttons.append(
            InlineKeyboardButton(
                text="◀",
                callback_data=build_callback(page - 1),
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=f"{page}/{pages}",
            callback_data=build_callback(page),
        )
    )

    if page < pages:
        buttons.append(
            InlineKeyboardButton(
                text="▶",
                callback_data=build_callback(page + 1),
            )
        )

    builder.row(*buttons)


def _toggle_on_filter(
    current: int,
    *,
    on_value: int = 1,
) -> int:
    return FILTER_ALL if current == on_value else on_value


def append_link_filter_options(
    builder: InlineKeyboardBuilder,
    *,
    is_active: int,
    backup_active: int,
) -> None:
    active_on = is_active == 1
    inactive_on = is_active == 0

    builder.row(
        InlineKeyboardButton(
            text=f"🟢 Активные {'✅' if active_on else '⬜'}",
            callback_data=NavigationCD(
                level=NavLevel.LINKS_FILTERS,
                fa=_toggle_on_filter(is_active, on_value=1),
                bfa=backup_active,
            ).pack(),
        ),
        InlineKeyboardButton(
            text=f"🔴 Неактивные {'✅' if inactive_on else '⬜'}",
            callback_data=NavigationCD(
                level=NavLevel.LINKS_FILTERS,
                fa=_toggle_on_filter(is_active, on_value=0),
                bfa=backup_active,
            ).pack(),
        ),
    )


def append_partner_filter_options(
    builder: InlineKeyboardBuilder,
    *,
    is_tracking: int,
    is_selected: int,
    backup_tracking: int,
    backup_selected: int,
) -> None:
    tracking_on = is_tracking == 1
    selected_on = is_selected == 1

    builder.row(
        InlineKeyboardButton(
            text=f"🔔 Трекинг {'✅' if tracking_on else '⬜'}",
            callback_data=NavigationCD(
                level=NavLevel.PARTNERS_FILTERS,
                ft=_toggle_on_filter(is_tracking, on_value=1),
                fs=is_selected,
                bft=backup_tracking,
                bfs=backup_selected,
            ).pack(),
        ),
        InlineKeyboardButton(
            text=f"⭐ Избранное {'✅' if selected_on else '⬜'}",
            callback_data=NavigationCD(
                level=NavLevel.PARTNERS_FILTERS,
                ft=is_tracking,
                fs=_toggle_on_filter(is_selected, on_value=1),
                bft=backup_tracking,
                bfs=backup_selected,
            ).pack(),
        ),
    )


def link_filters_button_text(is_active: int) -> str:
    if is_active == FILTER_ALL:
        return "🔍 Фильтры"

    if is_active == 1:
        return "🔍 Фильтры • 🟢"

    return "🔍 Фильтры • 🔴"


def partner_filters_button_text(
    is_tracking: int,
    is_selected: int,
) -> str:
    if is_tracking != 1 and is_selected != 1:
        return "🔍 Фильтры"

    parts: list[str] = []

    if is_tracking == 1:
        parts.append("🔔")

    if is_selected == 1:
        parts.append("⭐")

    return f"🔍 Фильтры • {' '.join(parts)}"

def build_form_prompt(
    text: str,
    cancel_data,
) -> tuple[str, InlineKeyboardMarkup]:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data=(
                cancel_data.pack()
                if isinstance(cancel_data, CallbackData)
                else cancel_data
            ),
        )
    )

    return text, builder.as_markup()
