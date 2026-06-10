# packages

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application dependencies

from ..callbacks import NavCD, LinkCD, OfferCD

from ..views.pagination import append_list_pagination

from ..utils import safe

from ...domain.types import OfferSummary


def build_offers_list(
    offers: list[OfferSummary],
    *,
    page: int = 1,
    pages: int = 1,
    total: int = 0,
) -> tuple[str, InlineKeyboardBuilder]:
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

    append_list_pagination(
        builder,
        level="offers",
        page=page,
        pages=pages,
    )

    builder.button(
        text="🏠 Главное меню",
        callback_data=NavCD(level="main"),
    )
    builder.adjust(1)

    if total:
        text = f"🎁 <b>Список офферов</b> ({total})"
    elif offers:
        text = "🎁 <b>Список офферов:</b>"
    else:
        text = "🎁 <b>Офферов пока нет.</b>"

    if pages > 1:
        text += f"\nСтраница {page} из {pages}"

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
