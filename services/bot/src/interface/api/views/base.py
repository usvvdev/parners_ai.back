# packages

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application depencies

from ..dto.callback import NavigationCD

from ....core.constants import (
    FILTER_ALL,
    PAGINATION_GRID_SIZE,
)

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


def _page_window(
    page: int,
    pages: int,
    *,
    width: int = 7,
) -> list[int]:
    if pages <= width:
        return list(range(1, pages + 1))

    half = width // 2
    start = max(1, page - half)
    end = min(pages, start + width - 1)
    start = max(1, end - width + 1)

    return list(range(start, end + 1))


def _append_page_grid(
    builder: InlineKeyboardBuilder,
    *,
    page: int,
    pages: int,
    build_callback,
    row_size: int = PAGINATION_GRID_SIZE,
) -> None:
    if pages <= 1:
        return

    nav_row: list[InlineKeyboardButton] = []

    if page > 1:
        nav_row.append(
            InlineKeyboardButton(
                text="◀️",
                callback_data=build_callback(page - 1),
            )
        )

    for page_number in _page_window(page, pages):
        nav_row.append(
            InlineKeyboardButton(
                text=f"· {page_number} ·" if page_number == page else str(page_number),
                callback_data=build_callback(page_number),
            )
        )

    if page < pages:
        nav_row.append(
            InlineKeyboardButton(
                text="▶️",
                callback_data=build_callback(page + 1),
            )
        )

    for index in range(0, len(nav_row), row_size):
        builder.row(*nav_row[index : index + row_size])


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
    _append_page_grid(
        builder,
        page=page,
        pages=pages,
        build_callback=lambda target_page: NavigationCD(
            level=level,
            page=target_page,
            fa=fa,
            ft=ft,
            fs=fs,
        ).pack(),
    )


def append_detail_pagination(
    builder: InlineKeyboardBuilder,
    *,
    page: int,
    pages: int,
    build_callback,
) -> None:
    _append_page_grid(
        builder,
        page=page,
        pages=pages,
        build_callback=build_callback,
    )


def append_link_filters(
    builder: InlineKeyboardBuilder,
    *,
    is_active: int,
    page: int,
) -> None:
    options = (
        ("Все", FILTER_ALL),
        ("🟢 Активные", 1),
        ("🔴 Неактивные", 0),
    )

    builder.row(
        *[
            InlineKeyboardButton(
                text=f"• {label} •" if is_active == value else label,
                callback_data=NavigationCD(
                    level=NavLevel.LINKS,
                    page=1 if value != is_active else page,
                    fa=value,
                ).pack(),
            )
            for label, value in options
        ]
    )


def append_partner_filters(
    builder: InlineKeyboardBuilder,
    *,
    is_tracking: int,
    is_selected: int,
    page: int,
) -> None:
    tracking_options = (
        ("Все", FILTER_ALL),
        ("🔔 Трекинг", 1),
        ("🔕 Без трекинга", 0),
    )
    selected_options = (
        ("Все", FILTER_ALL),
        ("⭐ Избранные", 1),
        ("☆ Остальные", 0),
    )

    builder.row(
        *[
            InlineKeyboardButton(
                text=f"• {label} •" if is_tracking == value else label,
                callback_data=NavigationCD(
                    level=NavLevel.PARTNERS,
                    page=1 if value != is_tracking else page,
                    ft=value,
                    fs=is_selected,
                ).pack(),
            )
            for label, value in tracking_options
        ]
    )
    builder.row(
        *[
            InlineKeyboardButton(
                text=f"• {label} •" if is_selected == value else label,
                callback_data=NavigationCD(
                    level=NavLevel.PARTNERS,
                    page=1 if value != is_selected else page,
                    ft=is_tracking,
                    fs=value,
                ).pack(),
            )
            for label, value in selected_options
        ]
    )


def build_form_prompt(
    text: str,
    cancel_data,
) -> tuple[str, InlineKeyboardMarkup]:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data=cancel_data,
        )
    )

    return text, builder.as_markup()
