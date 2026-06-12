from __future__ import annotations

# packages

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
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        builder.button(
            text="➕ Добавить Витрину",
            callback_data=LinkCD(action=LinkAction.CREATE, p_id=0, l_id=0),
        )

        for link in data.items:
            status = "🟢" if link.is_active else "🔴"
            builder.button(
                text=f"{status}{format_link_list_label(link.link, link.offers)}",
                callback_data=LinkCD(action=LinkAction.VIEW, p_id=0, l_id=link.id),
            )

        append_list_pagination(
            builder,
            level=NavLevel.LINKS,
            page=data.page,
            pages=data.pages,
        )

        builder.button(
            text="🏠 Главное меню",
            callback_data=NavigationCD(level=NavLevel.MAIN),
        )
        builder.adjust(1)

        text = build_list_text(
            data,
            title="🔗 <b>Список витрин</b>",
            empty="🔗 <b>Витрин пока нет.</b>",
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
        builder.button(
            text=toggle_text,
            callback_data=LinkCD(action=LinkAction.TOGGLE, p_id=p_id, l_id=link.id),
        )
        builder.button(
            text="✏️ Изменить офферы",
            callback_data=LinkCD(
                action=LinkAction.EDIT_OFFERS,
                p_id=p_id,
                l_id=link.id,
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
                ),
            )

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

        builder.button(
            text="🗑 Удалить витрину",
            callback_data=LinkCD(action=LinkAction.DELETE, p_id=p_id, l_id=link.id),
        )

        if p_id:
            builder.button(
                text="🔙 Назад к партнеру",
                callback_data=PartnerCD(action=PartnerAction.VIEW, p_id=p_id),
            )
        else:
            builder.button(
                text="🔙 Назад к витринам",
                callback_data=NavigationCD(level=NavLevel.LINKS),
            )

        builder.adjust(1)

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
                text=f"{status} {format_offer_button_label(symbol=offer.symbol, title=offer.title)}",
                callback_data=OfferCD(
                    action=OfferAction.PICK_TOGGLE,
                    p_id=p_id,
                    l_id=l_id,
                    o_id=offer.id,
                    page=data.page,
                ),
            )

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

        builder.button(
            text="✅ Готово",
            callback_data=OfferCD(
                action=OfferAction.PICK_CONFIRM,
                p_id=p_id,
                l_id=l_id,
                o_id=0,
                page=data.page,
            ),
        )
        builder.button(
            text="❌ Отмена",
            callback_data=OfferCD(
                action=OfferAction.PICK_CANCEL,
                p_id=p_id,
                l_id=l_id,
                o_id=0,
                page=data.page,
            ),
        )
        builder.adjust(1)

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
