# packages

from aiogram import Router, F

from aiogram.types import CallbackQuery

from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx import HTTPStatusError

# application dependencies

from ..callbacks import LinkCD, OfferCD

from ...infrastructure.clients.api import OfferAPIClient


router = Router()


@router.callback_query(OfferCD.filter(F.action == "view"))
async def show_offer(
    callback: CallbackQuery,
    callback_data: OfferCD,
    offer_client: OfferAPIClient,
) -> None:
    try:
        offer = await offer_client.fetch_by_id(callback_data.o_id)
    except HTTPStatusError:
        await callback.answer("Оффер не найден", show_alert=True)
        return

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔙 Назад к ссылке",
        callback_data=LinkCD(
            action="view",
            p_id=callback_data.p_id,
            l_id=callback_data.l_id,
        ),
    )
    builder.adjust(1)

    await callback.message.edit_text(
        f"🎁 <b>Оффер:</b> {offer.title}\n"
        f"🆔 <b>ID:</b> {offer.id}",
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()
