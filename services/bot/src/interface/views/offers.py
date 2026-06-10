# packages

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application dependencies

from ..callbacks import NavCD, LinkCD, OfferCD

from ..utils import safe

from ...domain.types import OfferSummary


def build_offers_list(offers: list[OfferSummary]) -> tuple[str, InlineKeyboardBuilder]:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="➕ Добавить оффер",
        callback_data=OfferCD(action="create", p_id=0, l_id=0, o_id=0),
    )

    for offer in offers:
        builder.button(
            text=f"🎁 {offer.title}",
            callback_data=OfferCD(action="view", p_id=0, l_id=0, o_id=offer.id),
        )

    builder.button(
        text="🏠 Главное меню",
        callback_data=NavCD(level="main"),
    )
    builder.adjust(1)

    text = "🎁 <b>Список офферов:</b>" if offers else "🎁 <b>Офферов пока нет.</b>"

    return text, builder


def build_offer_detail(
    offer: OfferSummary,
    *,
    p_id: int,
    l_id: int,
) -> tuple[str, InlineKeyboardBuilder]:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🗑 Удалить оффер",
        callback_data=OfferCD(
            action="delete",
            p_id=p_id,
            l_id=l_id,
            o_id=offer.id,
        ),
    )
    builder.button(
        text="🔙 Назад к ссылке" if l_id else "🔙 Назад к офферам",
        callback_data=(
            LinkCD(action="view", p_id=p_id, l_id=l_id)
            if l_id
            else NavCD(level="offers")
        ),
    )
    builder.adjust(1)

    text = f"🎁 <b>Оффер:</b> {safe(offer.title)}\n🆔 <b>ID:</b> {offer.id}"

    return text, builder
