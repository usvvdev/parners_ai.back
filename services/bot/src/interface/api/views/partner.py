from __future__ import annotations

# packages

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application depencies

from ..dto.callback import (
    NavigationCD,
    PartnerCD,
    LinkCD,
)

from .base import (
    build_list_text,
    append_list_pagination,
    append_detail_pagination,
)

from ....domain.types.enums.actions import (
    PartnerAction,
    LinkAction,
)

from ....domain.types.enums.common import NavLevel

from ....infrastructure.utils import (
    safe,
    format_link_list_label,
)

from ....domain.types._types import (
    FetchPartner,
    FetchPartners,
    FetchLinks,
    PaginatedResponse,
)


class PartnerView:
    @staticmethod
    def list(
        data: PaginatedResponse[FetchPartner],
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        builder.button(
            text="➕ Добавить партнера",
            callback_data=PartnerCD(action=PartnerAction.CREATE, p_id=0),
        )

        for partner in data.items:
            status = "🟢" if partner.is_tracking else "🔴"
            favorite = "⭐ " if partner.is_selected else ""
            builder.button(
                text=f"{favorite}{status} {partner.wmid}",
                callback_data=PartnerCD(action=PartnerAction.VIEW, p_id=partner.id),
            )

        append_list_pagination(
            builder,
            level=NavLevel.PARTNERS,
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
            title="📂 <b>Список партнеров</b>",
            empty="📂 <b>Партнеров пока нет.</b>",
        )

        return text, builder

    @staticmethod
    def detail(
        partner: FetchPartners,
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        builder.button(
            text="⚙️ Статус и избранное",
            callback_data=PartnerCD(
                action=PartnerAction.SETTINGS,
                p_id=partner.id,
                is_tracking=int(partner.is_tracking),
                is_selected=int(partner.is_selected),
            ),
        )
        builder.button(
            text="✏️ Изменить витрины",
            callback_data=PartnerCD(action=PartnerAction.EDIT_LINKS, p_id=partner.id),
        )

        for link in partner.links.items:
            status = "🟢" if link.is_active else "🔴"
            builder.button(
                text=f"{status}{format_link_list_label(link.link, link.offers)}",
                callback_data=LinkCD(
                    action=LinkAction.VIEW,
                    p_id=partner.id,
                    l_id=link.id,
                ),
            )

        append_detail_pagination(
            builder,
            page=partner.links.page,
            pages=partner.links.pages,
            build_callback=lambda page: PartnerCD(
                action=PartnerAction.VIEW,
                p_id=partner.id,
                page=page,
            ).pack(),
        )

        builder.button(
            text="🗑 Удалить партнера",
            callback_data=PartnerCD(action=PartnerAction.DELETE, p_id=partner.id),
        )
        builder.button(
            text="🔙 Назад к партнерам",
            callback_data=NavigationCD(level=NavLevel.PARTNERS),
        )
        builder.adjust(1)

        text = (
            f"🏢 <b>Партнер:</b> {safe(partner.wmid)}\n"
            f"🏷 <b>UTM:</b> {safe(partner.utm_source)}\n"
            f"⭐ <b>Избранное:</b> {'Да' if partner.is_selected else 'Нет'}\n"
            f"📊 <b>Трекинг:</b> {'Активен' if partner.is_tracking else 'Выключен'}\n\n"
            f"🔗 <b>Витрины ({partner.links.total}):</b>"
        )

        return text, builder

    @staticmethod
    def settings(
        partner: FetchPartners,
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        favorite_text = (
            "⭐ Убрать из избранного"
            if partner.is_selected
            else "☆ Добавить в избранное"
        )
        builder.button(
            text=favorite_text,
            callback_data=PartnerCD(
                action=PartnerAction.TOGGLE_SELECTED,
                p_id=partner.id,
                is_tracking=int(partner.is_tracking),
                is_selected=int(partner.is_selected),
            ),
        )

        tracking_text = (
            "🔕 Выключить трекинг" if partner.is_tracking else "🔔 Включить трекинг"
        )
        builder.button(
            text=tracking_text,
            callback_data=PartnerCD(
                action=PartnerAction.TOGGLE_TRACKING,
                p_id=partner.id,
                is_tracking=int(partner.is_tracking),
                is_selected=int(partner.is_selected),
            ),
        )

        builder.button(
            text="🔙 Назад к партнеру",
            callback_data=PartnerCD(action=PartnerAction.VIEW, p_id=partner.id),
        )
        builder.adjust(1)

        text = (
            f"⚙️ <b>Настройки партнера:</b> {safe(partner.wmid)}\n\n"
            f"⭐ <b>Избранное:</b> {'Да' if partner.is_selected else 'Нет'}\n"
            f"📊 <b>Трекинг:</b> {'Активен' if partner.is_tracking else 'Выключен'}"
        )

        return text, builder

    @staticmethod
    def link_picker(
        data: PaginatedResponse[FetchLinks],
        selected_ids: set[int],
        *,
        p_id: int,
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        for link in data.items:
            status = "🟢" if link.id in selected_ids else "🔴"
            builder.button(
                text=f"{status}{format_link_list_label(link.link, link.offers, url_limit=24)}",
                callback_data=LinkCD(
                    action=LinkAction.PICK_TOGGLE,
                    p_id=p_id,
                    l_id=link.id,
                    page=data.page,
                ),
            )

        append_detail_pagination(
            builder,
            page=data.page,
            pages=data.pages,
            build_callback=lambda page: LinkCD(
                action=LinkAction.PICK_PAGE,
                p_id=p_id,
                l_id=0,
                page=page,
            ).pack(),
        )

        builder.button(
            text="✅ Готово",
            callback_data=LinkCD(
                action=LinkAction.PICK_CONFIRM,
                p_id=p_id,
                l_id=0,
                page=data.page,
            ),
        )
        builder.button(
            text="❌ Отмена",
            callback_data=LinkCD(
                action=LinkAction.PICK_CANCEL,
                p_id=p_id,
                l_id=0,
                page=data.page,
            ),
        )
        builder.adjust(1)

        if data.total:
            text = (
                f"🔗 <b>Выберите витрину партнера</b> ({data.total})\n"
                f"🟢 — привязана, 🔴 — не привязана"
            )
        else:
            text = (
                "🔗 <b>Витрин пока нет.</b>\n"
                "Создайте витрину в разделе «Список витрин» или нажмите «Готово» без выбора."
            )

        if data.pages > 1:
            text += f"\nСтраница {data.page} из {data.pages}"

        return text, builder
