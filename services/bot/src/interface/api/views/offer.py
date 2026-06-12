from __future__ import annotations

# packages

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application depencies

from ..dto.callback import (
    NavigationCD,
    LinkCD,
    OfferCD,
)

from .base import (
    build_list_text,
    append_list_pagination,
)

from ....domain.types.enums.actions import (
    LinkAction,
    OfferAction,
)

from ....domain.types.enums.common import NavLevel

from ....infrastructure.utils import safe

from ....domain.types._types import (
    FetchOffer,
    PaginatedResponse,
)


class OfferView:
    @staticmethod
    def list(
        data: PaginatedResponse[FetchOffer],
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        builder.button(
            text="➕ Добавить оффер",
            callback_data=OfferCD(
                action=OfferAction.CREATE,
                p_id=0,
                l_id=0,
                o_id=0,
            ),
        )

        for offer in data.items:
            builder.button(
                text=f"🎁 {offer.title}",
                callback_data=OfferCD(
                    action=OfferAction.VIEW,
                    p_id=0,
                    l_id=0,
                    o_id=offer.id,
                ),
            )

        append_list_pagination(
            builder,
            level=NavLevel.OFFERS,
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
            title="🎁 <b>Список офферов</b>",
            empty="🎁 <b>Офферов пока нет.</b>",
        )

        return text, builder

    @staticmethod
    def detail(
        offer: FetchOffer,
        *,
        p_id: int = 0,
        l_id: int = 0,
    ) -> tuple[str, InlineKeyboardBuilder]:
        builder = InlineKeyboardBuilder()

        builder.button(
            text="🗑 Удалить оффер",
            callback_data=OfferCD(
                action=OfferAction.DELETE,
                p_id=p_id,
                l_id=l_id,
                o_id=offer.id,
            ),
        )
        builder.button(
            text="🔙 Назад к ссылке" if l_id else "🔙 Назад к офферам",
            callback_data=(
                LinkCD(action=LinkAction.VIEW, p_id=p_id, l_id=l_id)
                if l_id
                else NavigationCD(level=NavLevel.OFFERS)
            ),
        )
        builder.adjust(1)

        text = f"🎁 <b>Оффер:</b> {safe(offer.title)}\n🆔 <b>ID:</b> {offer.id}"

        return text, builder
