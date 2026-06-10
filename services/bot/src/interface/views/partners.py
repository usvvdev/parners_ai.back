# packages

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application dependencies

from ..callbacks import NavCD, PartnerCD, LinkCD

from ..views.pagination import append_list_pagination

from ..utils import safe, short_url

from ...domain.types import Partner, PartnerDetail


def build_partners_list(
    partners: list[Partner],
    *,
    page: int = 1,
    pages: int = 1,
    total: int = 0,
) -> tuple[str, InlineKeyboardBuilder]:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="➕ Добавить партнера",
        callback_data=PartnerCD(action="create", p_id=0),
    )

    for partner in partners:
        status = "🟢" if partner.is_tracking else "🔴"
        favorite = "⭐ " if partner.is_selected else ""
        builder.button(
            text=f"{favorite}{status} {partner.wmid}",
            callback_data=PartnerCD(action="view", p_id=partner.id),
        )

    append_list_pagination(
        builder,
        level="partners",
        page=page,
        pages=pages,
    )

    builder.button(
        text="🏠 Главное меню",
        callback_data=NavCD(level="main"),
    )
    builder.adjust(1)

    if total:
        text = f"📂 <b>Список партнеров</b> ({total})"
    elif partners:
        text = "📂 <b>Список партнеров:</b>"
    else:
        text = "📂 <b>Партнеров пока нет.</b>"

    if pages > 1:
        text += f"\nСтраница {page} из {pages}"

    return text, builder


def build_partner_detail(partner: PartnerDetail) -> tuple[str, InlineKeyboardBuilder]:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="⚙️ Статус и избранное",
        callback_data=PartnerCD(
            action="settings",
            p_id=partner.id,
            is_tracking=int(partner.is_tracking),
            is_selected=int(partner.is_selected),
        ),
    )
    builder.button(
        text="➕ Добавить ссылку",
        callback_data=LinkCD(action="create_for_partner", p_id=partner.id, l_id=0),
    )
    builder.button(
        text="✏️ Изменить ссылки",
        callback_data=PartnerCD(action="edit_links", p_id=partner.id),
    )

    for link in partner.links:
        builder.button(
            text=f"🔗 {short_url(link.link)}",
            callback_data=LinkCD(action="view", p_id=partner.id, l_id=link.id),
        )

    builder.button(
        text="🗑 Удалить партнера",
        callback_data=PartnerCD(action="delete", p_id=partner.id),
    )
    builder.button(
        text="🔙 Назад к партнерам",
        callback_data=NavCD(level="partners"),
    )
    builder.adjust(1)

    text = (
        f"🏢 <b>Партнер:</b> {safe(partner.wmid)}\n"
        f"🏷 <b>UTM:</b> {safe(partner.utm_source)}\n"
        f"⭐ <b>Избранное:</b> {'Да' if partner.is_selected else 'Нет'}\n"
        f"📊 <b>Трекинг:</b> {'Активен' if partner.is_tracking else 'Выключен'}\n\n"
        f"🔗 <b>Ссылки ({len(partner.links)}):</b>"
    )

    return text, builder


def build_partner_settings(partner: PartnerDetail) -> tuple[str, InlineKeyboardBuilder]:
    builder = InlineKeyboardBuilder()

    favorite_text = (
        "⭐ Убрать из избранного" if partner.is_selected else "☆ Добавить в избранное"
    )
    builder.button(
        text=favorite_text,
        callback_data=PartnerCD(
            action="toggle_selected",
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
            action="toggle_tracking",
            p_id=partner.id,
            is_tracking=int(partner.is_tracking),
            is_selected=int(partner.is_selected),
        ),
    )

    builder.button(
        text="🔙 Назад к партнеру",
        callback_data=PartnerCD(action="view", p_id=partner.id),
    )
    builder.adjust(1)

    text = (
        f"⚙️ <b>Настройки партнера:</b> {safe(partner.wmid)}\n\n"
        f"⭐ <b>Избранное:</b> {'Да' if partner.is_selected else 'Нет'}\n"
        f"📊 <b>Трекинг:</b> {'Активен' if partner.is_tracking else 'Выключен'}"
    )

    return text, builder


def build_link_picker(
    links: list,
    selected_ids: set[int],
    *,
    p_id: int,
) -> tuple[str, InlineKeyboardBuilder]:
    builder = InlineKeyboardBuilder()

    for link in links:
        status = "🟢" if link.id in selected_ids else "🔴"
        builder.button(
            text=f"{status} {short_url(link.link)}",
            callback_data=LinkCD(
                action="link_pick_toggle",
                p_id=p_id,
                l_id=link.id,
            ),
        )

    builder.button(
        text="✅ Готово",
        callback_data=LinkCD(
            action="link_pick_confirm",
            p_id=p_id,
            l_id=0,
        ),
    )
    builder.button(
        text="❌ Отмена",
        callback_data=LinkCD(
            action="link_pick_cancel",
            p_id=p_id,
            l_id=0,
        ),
    )
    builder.adjust(1)

    text = "🔗 <b>Выберите ссылки партнера</b>\n🟢 — привязана, 🔴 — не привязана"

    if not links:
        text = (
            "🔗 <b>Ссылок пока нет.</b>\n"
            "Создайте ссылку в разделе «Список ссылок» или нажмите «Готово» без выбора."
        )

    return text, builder
