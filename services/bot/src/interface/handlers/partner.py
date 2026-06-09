# packages

from aiogram import Router, F

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message

from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx import HTTPStatusError

# application dependencies

from ..callbacks import NavCD, PartnerCD, LinkCD

from ..states import PartnerForm, LinkForm

from ..utils import safe, short_url, parse_ids

from ...domain.types import PartnerDetail

from ...infrastructure.clients.api import PartnerAPIClient, LinkAPIClient


router = Router()


def _partner_keyboard(partner: PartnerDetail) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    toggle_text = (
        "🔕 Выключить трекинг" if partner.is_tracking else "🔔 Включить трекинг"
    )
    builder.button(
        text=toggle_text,
        callback_data=PartnerCD(
            action="toggle",
            p_id=partner.id,
            is_tracking=int(partner.is_tracking),
        ),
    )
    builder.button(
        text="➕ Добавить ссылку",
        callback_data=LinkCD(action="create_for_partner", p_id=partner.id, l_id=0),
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

    return builder


async def _render_partner(
    callback: CallbackQuery,
    partner: PartnerDetail,
) -> None:
    builder = _partner_keyboard(partner)

    await callback.message.edit_text(
        f"🏢 <b>Партнер:</b> {safe(partner.wmid)}\n"
        f"🏷 <b>UTM:</b> {safe(partner.utm_source)}\n"
        f"📊 <b>Трекинг:</b> {'Активен' if partner.is_tracking else 'Выключен'}\n\n"
        f"🔗 <b>Ссылки ({len(partner.links)}):</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )


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

    builder = InlineKeyboardBuilder()
    builder.button(
        text="➕ Добавить партнера",
        callback_data=PartnerCD(action="create", p_id=0),
    )

    for p in partners:
        status = "🟢" if p.is_tracking else "🔴"
        builder.button(
            text=f"{status} {p.wmid}",
            callback_data=PartnerCD(action="view", p_id=p.id),
        )

    builder.button(
        text="🏠 Главное меню",
        callback_data=NavCD(level="main"),
    )

    builder.adjust(1)

    await callback.message.edit_text(
        "📂 <b>Список партнеров:</b>" if partners else "📂 <b>Партнеров пока нет.</b>",
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

    await _render_partner(callback, partner)
    await callback.answer()


@router.callback_query(PartnerCD.filter(F.action == "create"))
async def create_partner_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(PartnerForm.create_wmid)
    await callback.message.answer("Введите WMID партнера:")
    await callback.answer()


@router.message(PartnerForm.create_wmid)
async def create_partner_wmid(
    message: Message,
    state: FSMContext,
) -> None:
    await state.update_data(wmid=message.text.strip())
    await state.set_state(PartnerForm.create_utm_source)
    await message.answer("Введите UTM source партнера:")


@router.message(PartnerForm.create_utm_source)
async def create_partner_finish(
    message: Message,
    state: FSMContext,
    partner_client: PartnerAPIClient,
) -> None:
    data = await state.get_data()
    await state.clear()

    try:
        partner = await partner_client.create(
            {
                "wmid": data["wmid"],
                "utm_source": message.text.strip(),
                "is_tracking": True,
                "link_ids": [],
            }
        )
    except HTTPStatusError:
        await message.answer("Не удалось создать партнера")
        return

    await message.answer(
        f"Партнер создан: <b>{safe(partner.wmid)}</b>", parse_mode="HTML"
    )


@router.callback_query(PartnerCD.filter(F.action == "toggle"))
async def toggle_partner(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_client: PartnerAPIClient,
) -> None:
    new_status = not bool(callback_data.is_tracking)

    try:
        partner = await partner_client.update(
            callback_data.p_id,
            {"is_tracking": new_status},
        )
    except HTTPStatusError:
        await callback.answer("Ошибка обновления статуса", show_alert=True)
        return

    status_text = "включен" if new_status else "выключен"
    await callback.answer(f"Трекинг {status_text}")
    await _render_partner(callback, partner)


@router.callback_query(PartnerCD.filter(F.action == "delete"))
async def delete_partner(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_client: PartnerAPIClient,
) -> None:
    try:
        await partner_client.delete(callback_data.p_id)
    except HTTPStatusError:
        await callback.answer("Не удалось удалить партнера", show_alert=True)
        return

    await callback.answer("Партнер удален")
    await show_partners(callback, partner_client)


@router.callback_query(LinkCD.filter(F.action == "create_for_partner"))
async def create_partner_link_start(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
) -> None:
    await state.update_data(p_id=callback_data.p_id)
    await state.set_state(LinkForm.create_url)
    await callback.message.answer("Введите URL новой ссылки:")
    await callback.answer()


@router.message(LinkForm.create_url)
async def create_link_url(
    message: Message,
    state: FSMContext,
) -> None:
    await state.update_data(link=message.text.strip())
    await state.set_state(LinkForm.create_offer_ids)
    await message.answer(
        "Введите ID офферов через запятую или '-' если офферов пока нет:"
    )


@router.message(LinkForm.create_offer_ids)
async def create_link_finish(
    message: Message,
    state: FSMContext,
    link_client: LinkAPIClient,
    partner_client: PartnerAPIClient,
) -> None:
    data = await state.get_data()
    await state.clear()

    try:
        offer_ids = parse_ids(message.text)
    except ValueError:
        await message.answer("ID офферов должны быть числами через запятую")
        return

    try:
        link = await link_client.create(
            {
                "link": data["link"],
                "is_active": True,
                "offer_ids": offer_ids,
            }
        )

        p_id = data.get("p_id")
        if p_id:
            partner = await partner_client.fetch_by_id(p_id)
            link_ids = [item.id for item in partner.links]
            await partner_client.update(
                p_id,
                {"link_ids": [*link_ids, link.id]},
            )
    except HTTPStatusError:
        await message.answer("Не удалось создать или привязать ссылку")
        return

    await message.answer(
        f"Ссылка создана: <b>{safe(short_url(link.link))}</b>", parse_mode="HTML"
    )
