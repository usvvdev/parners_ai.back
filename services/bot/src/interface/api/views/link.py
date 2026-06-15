from __future__ import annotations

# packages

from aiogram.types import InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application depencies

from ..dto.callback import (
    NavigationCD,
    PartnerCD,
    LinkCD,
    OfferCD,
)

from .base import (
    build_list_text,
    append_list_pagination,
    append_detail_pagination,
    append_link_filter_options,
    append_item_grid,
    link_filters_button_text,
)

from ....core.constants import (
    FILTER_ALL,
    LIST_GRID_URL_LIMIT,
)

from ....domain.types.enums.actions import (
    PartnerAction,
    LinkAction,
    OfferAction,
)

from ....domain.types.enums.common import (
    NavLevel,
    PickMode,
)

from ....infrastructure.utils import (
    safe,
    short_url,
    format_offer_symbols,
    format_offer_button_label,
    format_link_list_label,
)

from ....domain.types._types import (
    FetchLinks,
    FetchLink,
    FetchOffer,
    PaginatedResponse,
)


class LinkView:
    @staticmethod
    def list(
        data: PaginatedResponse[FetchLinks],
        *,
        is_active: int = FILTER_ALL,
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        builder.row(
            InlineKeyboardButton(
                text="➕ Добавить Витрину",
                callback_data=LinkCD(
                    action=LinkAction.CREATE,
                    p_id=0,
                    l_id=0,
                ).pack(),
            ),
            InlineKeyboardButton(
                text=link_filters_button_text(is_active),
                callback_data=NavigationCD(
                    level=NavLevel.LINKS_FILTERS,
                    fa=is_active,
                    bfa=is_active,
                ).pack(),
            ),
        )

        for link in data.items:
            status = "🟢" if link.is_active else "🔴"
            builder.button(
                text=f"{status}{format_link_list_label(link.link, link.offers, url_limit=LIST_GRID_URL_LIMIT)}",
                callback_data=LinkCD(
                    action=LinkAction.VIEW,
                    p_id=0,
                    l_id=link.id,
                ).pack(),
            )

        append_item_grid(builder, count=len(data.items))

        append_list_pagination(
            builder,
            level=NavLevel.LINKS,
            page=data.page,
            pages=data.pages,
            fa=is_active,
        )

        builder.row(
            InlineKeyboardButton(
                text="🏠 Главное меню",
                callback_data=NavigationCD(level=NavLevel.MAIN).pack(),
            )
        )

        text = build_list_text(
            data,
            title="🔗 <b>Список витрин</b>",
            empty="🔗 <b>Витрин пока нет.</b>",
        )

        return text, builder

    @staticmethod
    def filters(
        *,
        is_active: int = FILTER_ALL,
        backup_active: int = FILTER_ALL,
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        append_link_filter_options(
            builder,
            is_active=is_active,
            backup_active=backup_active,
        )

        builder.row(
            InlineKeyboardButton(
                text="✅ Показать",
                callback_data=NavigationCD(
                    level=NavLevel.LINKS,
                    page=1,
                    fa=is_active,
                    pr=0,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=NavigationCD(
                    level=NavLevel.LINKS,
                    page=1,
                    fa=backup_active,
                    pr=0,
                ).pack(),
            ),
        )

        text = (
            "🔍 <b>Фильтры витрин</b>\n\n"
            "🟢 <b>Активные</b> и 🔴 <b>неактивные</b>"
        )

        return text, builder

    @staticmethod
    def detail(
        link: FetchLink,
        *,
        p_id: int = 0,
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        toggle_text = "❌ Деактивировать" if link.is_active else "✅ Активировать"
        builder.row(
            InlineKeyboardButton(
                text=toggle_text,
                callback_data=LinkCD(
                    action=LinkAction.TOGGLE,
                    p_id=p_id,
                    l_id=link.id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="✏️ Изменить офферы",
                callback_data=LinkCD(
                    action=LinkAction.EDIT_OFFERS,
                    p_id=p_id,
                    l_id=link.id,
                ).pack(),
            ),
        )

        for offer in link.offers.items:
            builder.button(
                text=format_offer_button_label(
                    symbol=offer.symbol,
                    title=offer.title,
                ),
                callback_data=OfferCD(
                    action=OfferAction.VIEW,
                    p_id=p_id,
                    l_id=link.id,
                    o_id=offer.id,
                ).pack(),
            )

        append_item_grid(builder, count=len(link.offers.items))

        append_detail_pagination(
            builder,
            page=link.offers.page,
            pages=link.offers.pages,
            build_callback=lambda page: LinkCD(
                action=LinkAction.VIEW,
                p_id=p_id,
                l_id=link.id,
                page=page,
            ).pack(),
        )

        builder.row(
            InlineKeyboardButton(
                text="🗑 Удалить витрину",
                callback_data=LinkCD(
                    action=LinkAction.DELETE,
                    p_id=p_id,
                    l_id=link.id,
                ).pack(),
            )
        )

        if p_id:
            builder.row(
                InlineKeyboardButton(
                    text="🔙 Назад к партнеру",
                    callback_data=PartnerCD(
                        action=PartnerAction.VIEW,
                        p_id=p_id,
                    ).pack(),
                )
            )
        else:
            builder.row(
                InlineKeyboardButton(
                    text="🔙 Назад к витринам",
                    callback_data=NavigationCD(level=NavLevel.LINKS).pack(),
                )
            )

        text = (
            f"🔗 <b>Витрина:</b> {safe(short_url(link.link, limit=80))}\n"
            f"⚡ <b>Статус:</b> {'🟢 Активна' if link.is_active else '🔴 Отключена'}\n"
            f"🏷 <b>Офферы:</b> {format_offer_symbols([o.symbol for o in link.offers.items if o.symbol])}\n\n"
            f"📋 <b>Список ({link.offers.total}):</b>"
        )

        return text, builder

    @staticmethod
    def offer_picker(
        data: PaginatedResponse[FetchOffer],
        selected_ids: set[int],
        *,
        p_id: int,
        l_id: int,
        mode: str,
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        for offer in data.items:
            status = "🟢" if offer.id in selected_ids else "🔴"
            builder.button(
                text=f"{status}{format_offer_button_label(symbol=offer.symbol, title=offer.title)}",
                callback_data=OfferCD(
                    action=OfferAction.PICK_TOGGLE,
                    p_id=p_id,
                    l_id=l_id,
                    o_id=offer.id,
                    page=data.page,
                ).pack(),
            )

        append_item_grid(builder, count=len(data.items))

        append_detail_pagination(
            builder,
            page=data.page,
            pages=data.pages,
            build_callback=lambda page: OfferCD(
                action=OfferAction.PICK_PAGE,
                p_id=p_id,
                l_id=l_id,
                o_id=0,
                page=page,
            ).pack(),
        )

        builder.row(
            InlineKeyboardButton(
                text="✅ Готово",
                callback_data=OfferCD(
                    action=OfferAction.PICK_CONFIRM,
                    p_id=p_id,
                    l_id=l_id,
                    o_id=0,
                    page=data.page,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data=OfferCD(
                    action=OfferAction.PICK_CANCEL,
                    p_id=p_id,
                    l_id=l_id,
                    o_id=0,
                    page=data.page,
                ).pack(),
            ),
        )

        action_text = "создания" if mode == PickMode.CREATE else "редактирования"

        if data.total:
            text = (
                f"📋 <b>Выберите офферы для {action_text} ссылки</b> ({data.total})\n"
                f"🟢 — выбран, 🔴 — не выбран"
            )
        else:
            text = (
                "📋 <b>Офферов пока нет.</b>\n"
                "Создайте оффер в разделе «Список офферов» или нажмите «Готово» без выбора."
            )

        if data.pages > 1:
            text += f"\nСтраница {data.page} из {data.pages}"

        return text, builder
