# packages

from aiogram import Router, F

from aiogram.types import CallbackQuery

from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx import HTTPStatusError

# application dependencies

from ..callbacks import NavCD, PartnerCD, LinkCD

from ...infrastructure.clients.api import PartnerAPIClient


router = Router()


@router.callback_query(NavCD.filter(F.level == "partners"))
async def show_partners(
    callback: CallbackQuery,
    partner_client: PartnerAPIClient,
) -> None:
    try:
        partners = await partner_client.fetch_all()
    except HTTPStatusError:
        await callback.answer("Ошибка загрузки партнеров", show_alert=True)
        return

    if not partners:
        await callback.answer("Список партнеров пуст", show_alert=True)
        return

    builder = InlineKeyboardBuilder()

    for p in partners:
        status = "🟢" if p.is_tracking else "🔴"
        builder.button(
            text=f"{status} {p.wmid}",
            callback_data=PartnerCD(action="view", p_id=p.id),
        )

    builder.adjust(1)

    await callback.message.edit_text(
        "📂 <b>Список партнеров:</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(PartnerCD.filter(F.action == "view"))
async def show_partner(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_client: PartnerAPIClient,
) -> None:
    try:
        partner = await partner_client.fetch_by_id(callback_data.p_id)
    except HTTPStatusError:
        await callback.answer("Партнер не найден", show_alert=True)
        return

    builder = InlineKeyboardBuilder()

    toggle_text = (
        "🔕 Выключить трекинг" if partner.is_tracking else "🔔 Включить трекинг"
    )
    builder.button(
        text=toggle_text,
        callback_data=PartnerCD(action="toggle", p_id=partner.id),
    )

    for link in partner.links:
        short_url = link.link.replace("https://", "").replace("http://", "")[:25]
        builder.button(
            text=f"🔗 {short_url}",
            callback_data=LinkCD(action="view", p_id=partner.id, l_id=link.id),
        )

    builder.button(
        text="🔙 Назад к партнерам",
        callback_data=NavCD(level="partners"),
    )
    builder.adjust(1)

    await callback.message.edit_text(
        f"🏢 <b>Партнер:</b> {partner.wmid}\n"
        f"📊 <b>Трекинг:</b> {'Активен' if partner.is_tracking else 'Выключен'}\n\n"
        f"🔗 <b>Ссылки ({len(partner.links)}):</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(PartnerCD.filter(F.action == "toggle"))
async def toggle_partner(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_client: PartnerAPIClient,
) -> None:
    try:
        partner = await partner_client.fetch_by_id(callback_data.p_id)
        new_status = not partner.is_tracking

        await partner_client.update(
            callback_data.p_id,
            {"is_tracking": new_status},
        )
    except HTTPStatusError:
        await callback.answer("Ошибка обновления статуса", show_alert=True)
        return

    status_text = "включен" if new_status else "выключен"
    await callback.answer(f"Трекинг {status_text}")

    await show_partner(
        callback,
        PartnerCD(action="view", p_id=callback_data.p_id),
        partner_client,
    )
