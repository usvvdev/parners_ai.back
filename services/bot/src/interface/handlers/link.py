# packages

from aiogram import Router, F

from aiogram.types import CallbackQuery

from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx import HTTPStatusError

# application dependencies

from ..callbacks import PartnerCD, LinkCD, OfferCD

from ...infrastructure.clients.api import LinkAPIClient


router = Router()


@router.callback_query(LinkCD.filter(F.action == "view"))
async def show_link(
    callback: CallbackQuery,
    callback_data: LinkCD,
    link_client: LinkAPIClient,
) -> None:
    try:
        link = await link_client.fetch_by_id(callback_data.l_id)
    except HTTPStatusError:
        await callback.answer("Ссылка не найдена", show_alert=True)
        return

    builder = InlineKeyboardBuilder()

    toggle_text = "❌ Деактивировать" if link.is_active else "✅ Активировать"
    builder.button(
        text=toggle_text,
        callback_data=LinkCD(
            action="toggle",
            p_id=callback_data.p_id,
            l_id=link.id,
        ),
    )

    for offer in link.offers:
        builder.button(
            text=f"🎁 {offer.title}",
            callback_data=OfferCD(
                action="view",
                p_id=callback_data.p_id,
                l_id=link.id,
                o_id=offer.id,
            ),
        )

    builder.button(
        text="🔙 Назад к партнеру",
        callback_data=PartnerCD(action="view", p_id=callback_data.p_id),
    )
    builder.adjust(1)

    short_url = link.link.replace("https://", "").replace("http://", "")

    await callback.message.edit_text(
        f"🔗 <b>Ссылка:</b> {short_url}\n"
        f"⚡ <b>Статус:</b> {'Активна' if link.is_active else 'Отключена'}\n\n"
        f"🎁 <b>Офферы ({len(link.offers)}):</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(LinkCD.filter(F.action == "toggle"))
async def toggle_link(
    callback: CallbackQuery,
    callback_data: LinkCD,
    link_client: LinkAPIClient,
) -> None:
    try:
        link = await link_client.fetch_by_id(callback_data.l_id)
        new_status = not link.is_active

        await link_client.update(
            callback_data.l_id,
            {"is_active": new_status},
        )
    except HTTPStatusError:
        await callback.answer("Ошибка обновления статуса", show_alert=True)
        return

    status_text = "активирована" if new_status else "деактивирована"
    await callback.answer(f"Ссылка {status_text}")

    await show_link(
        callback,
        LinkCD(action="view", p_id=callback_data.p_id, l_id=callback_data.l_id),
        link_client,
    )
