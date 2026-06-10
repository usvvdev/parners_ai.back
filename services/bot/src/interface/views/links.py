# packages

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application dependencies

from ..callbacks import NavCD, PartnerCD, LinkCD, OfferCD

from ..utils import safe, short_url

from ...domain.types import LinkSummary, LinkDetail, OfferSummary


def build_links_list(links: list[LinkSummary]) -> tuple[str, InlineKeyboardBuilder]:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="➕ Добавить ссылку",
        callback_data=LinkCD(action="create", p_id=0, l_id=0),
    )

    for link in links:
        builder.button(
            text=f"🔗 {short_url(link.link)}",
            callback_data=LinkCD(action="view", p_id=0, l_id=link.id),
        )

    builder.button(
        text="🏠 Главное меню",
        callback_data=NavCD(level="main"),
    )
    builder.adjust(1)

    text = "🔗 <b>Список ссылок:</b>" if links else "🔗 <b>Ссылок пока нет.</b>"

    return text, builder


def build_link_detail(
    link: LinkDetail,
    p_id: int,
) -> tuple[str, InlineKeyboardBuilder]:
    builder = InlineKeyboardBuilder()

    toggle_text = "❌ Деактивировать" if link.is_active else "✅ Активировать"
    builder.button(
        text=toggle_text,
        callback_data=LinkCD(action="toggle", p_id=p_id, l_id=link.id),
    )
    builder.button(
        text="✏️ Изменить офферы",
        callback_data=LinkCD(action="edit_offers", p_id=p_id, l_id=link.id),
    )

    for offer in link.offers:
        builder.button(
            text=f"🎁 {offer.title}",
            callback_data=OfferCD(
                action="view",
                p_id=p_id,
                l_id=link.id,
                o_id=offer.id,
            ),
        )

    builder.button(
        text="🗑 Удалить ссылку",
        callback_data=LinkCD(action="delete", p_id=p_id, l_id=link.id),
    )

    if p_id:
        builder.button(
            text="🔙 Назад к партнеру",
            callback_data=PartnerCD(action="view", p_id=p_id),
        )
    else:
        builder.button(
            text="🔙 Назад к ссылкам",
            callback_data=NavCD(level="links"),
        )

    builder.adjust(1)

    text = (
        f"🔗 <b>Ссылка:</b> {safe(short_url(link.link, limit=80))}\n"
        f"⚡ <b>Статус:</b> {'Активна' if link.is_active else 'Отключена'}\n\n"
        f"🎁 <b>Офферы ({len(link.offers)}):</b>"
    )

    return text, builder


def build_offer_picker(
    offers: list[OfferSummary],
    selected_ids: set[int],
    *,
    p_id: int,
    l_id: int,
    mode: str,
) -> tuple[str, InlineKeyboardBuilder]:
    builder = InlineKeyboardBuilder()

    for offer in offers:
        status = "🟢" if offer.id in selected_ids else "🔴"
        builder.button(
            text=f"{status} {offer.title}",
            callback_data=OfferCD(
                action="pick_toggle",
                p_id=p_id,
                l_id=l_id,
                o_id=offer.id,
            ),
        )

    builder.button(
        text="✅ Готово",
        callback_data=OfferCD(
            action="pick_confirm",
            p_id=p_id,
            l_id=l_id,
            o_id=0,
        ),
    )
    builder.button(
        text="❌ Отмена",
        callback_data=OfferCD(
            action="pick_cancel",
            p_id=p_id,
            l_id=l_id,
            o_id=0,
        ),
    )
    builder.adjust(1)

    action_text = "создания" if mode == "create" else "редактирования"
    text = (
        f"🎁 <b>Выберите офферы для {action_text} ссылки</b>\n"
        f"🟢 — выбран, 🔴 — не выбран"
    )

    if not offers:
        text = (
            "🎁 <b>Офферов пока нет.</b>\n"
            "Создайте оффер в разделе «Список офферов» или нажмите «Готово» без выбора."
        )

    return text, builder
