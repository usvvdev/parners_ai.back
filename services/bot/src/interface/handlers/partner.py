# packages

from aiogram import Router, F

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message

from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx import HTTPStatusError

# application dependencies

from ..callbacks import NavCD, PartnerCD, LinkCD

from ..states import PartnerForm

from ..utils import (
    init_form_context,
    edit_menu_message,
    delete_user_message,
)

from ..views.partners import (
    build_partners_list,
    build_partner_detail,
    build_partner_settings,
    build_link_picker,
)

from ...infrastructure.clients.api import PartnerAPIClient, LinkAPIClient


router = Router()


async def _render_link_picker(
    bot,
    state: FSMContext,
    link_client: LinkAPIClient,
) -> None:
    data = await state.get_data()
    links = await link_client.fetch_all()
    selected_ids = set(data.get("selected_link_ids", []))

    text, builder = build_link_picker(
        links,
        selected_ids,
        p_id=data["p_id"],
    )

    await edit_menu_message(
        bot,
        state,
        text,
        builder.as_markup(),
    )


@router.callback_query(NavCD.filter(F.level == "partners"))
async def show_partners(
    callback: CallbackQuery,
    callback_data: NavCD,
    partner_client: PartnerAPIClient,
) -> None:
    try:
        result = await partner_client.fetch_page(page=callback_data.page)
    except HTTPStatusError:
        await callback.answer("Ошибка загрузки партнеров", show_alert=True)
        return

    text, builder = build_partners_list(
        result.items,
        page=result.page,
        pages=result.pages,
        total=result.total,
    )

    await callback.message.edit_text(
        text,
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

    text, builder = build_partner_detail(partner)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(PartnerCD.filter(F.action == "create"))
async def create_partner_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await init_form_context(state, callback)

    cancel = InlineKeyboardBuilder()
    cancel.button(
        text="❌ Отмена",
        callback_data=NavCD(level="partners"),
    )
    cancel.adjust(1)

    await edit_menu_message(
        callback.bot,
        state,
        "🏢 <b>Введите WMID партнера:</b>",
        cancel.as_markup(),
    )
    await state.set_state(PartnerForm.create_wmid)
    await callback.answer()


@router.message(PartnerForm.create_wmid)
async def create_partner_wmid(
    message: Message,
    state: FSMContext,
) -> None:
    await delete_user_message(message)
    await state.update_data(wmid=message.text.strip())

    cancel = InlineKeyboardBuilder()
    cancel.button(
        text="❌ Отмена",
        callback_data=NavCD(level="partners"),
    )
    cancel.adjust(1)

    await edit_menu_message(
        message.bot,
        state,
        "🏷 <b>Введите UTM source партнера:</b>",
        cancel.as_markup(),
    )
    await state.set_state(PartnerForm.create_utm_source)


@router.message(PartnerForm.create_utm_source)
async def create_partner_finish(
    message: Message,
    state: FSMContext,
    partner_client: PartnerAPIClient,
) -> None:
    await delete_user_message(message)

    data = await state.get_data()

    try:
        await partner_client.create(
            {
                "wmid": data["wmid"],
                "utm_source": message.text.strip(),
                "is_tracking": True,
                "is_selected": False,
                "link_ids": [],
            }
        )
        partners = await partner_client.fetch_page(page=1)
    except HTTPStatusError:
        await edit_menu_message(
            message.bot,
            state,
            "❌ Не удалось создать партнера",
        )
        await state.clear()
        return

    text, builder = build_partners_list(
        partners.items,
        page=partners.page,
        pages=partners.pages,
        total=partners.total,
    )
    await edit_menu_message(
        message.bot,
        state,
        text,
        builder.as_markup(),
    )
    await state.clear()


@router.callback_query(PartnerCD.filter(F.action == "settings"))
async def show_partner_settings(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_client: PartnerAPIClient,
) -> None:
    try:
        partner = await partner_client.fetch_by_id(callback_data.p_id)
    except HTTPStatusError:
        await callback.answer("Партнер не найден", show_alert=True)
        return

    text, builder = build_partner_settings(partner)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(PartnerCD.filter(F.action == "toggle_tracking"))
async def toggle_partner_tracking(
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
        await callback.answer("Ошибка обновления трекинга", show_alert=True)
        return

    status_text = "включен" if new_status else "выключен"
    await callback.answer(f"Трекинг {status_text}")

    text, builder = build_partner_settings(partner)
    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )


@router.callback_query(PartnerCD.filter(F.action == "toggle_selected"))
async def toggle_partner_selected(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_client: PartnerAPIClient,
) -> None:
    new_status = not bool(callback_data.is_selected)

    try:
        partner = await partner_client.update(
            callback_data.p_id,
            {"is_selected": new_status},
        )
    except HTTPStatusError:
        await callback.answer("Ошибка обновления избранного", show_alert=True)
        return

    status_text = "добавлен в избранное" if new_status else "убран из избранного"
    await callback.answer(status_text)

    text, builder = build_partner_settings(partner)
    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )


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


@router.callback_query(PartnerCD.filter(F.action == "edit_links"))
async def edit_partner_links_start(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    state: FSMContext,
    partner_client: PartnerAPIClient,
    link_client: LinkAPIClient,
) -> None:
    try:
        partner = await partner_client.fetch_by_id(callback_data.p_id)
    except HTTPStatusError:
        await callback.answer("Партнер не найден", show_alert=True)
        return

    await init_form_context(
        state,
        callback,
        p_id=callback_data.p_id,
        selected_link_ids=[link.id for link in partner.links],
    )
    await state.set_state(PartnerForm.select_links)
    await _render_link_picker(callback.bot, state, link_client)
    await callback.answer()


@router.callback_query(LinkCD.filter(F.action == "link_pick_toggle"))
async def link_pick_toggle(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    link_client: LinkAPIClient,
) -> None:
    data = await state.get_data()
    selected_ids = set(data.get("selected_link_ids", []))

    if callback_data.l_id in selected_ids:
        selected_ids.remove(callback_data.l_id)
    else:
        selected_ids.add(callback_data.l_id)

    await state.update_data(selected_link_ids=list(selected_ids))
    await _render_link_picker(callback.bot, state, link_client)
    await callback.answer()


@router.callback_query(LinkCD.filter(F.action == "link_pick_cancel"))
async def link_pick_cancel(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    partner_client: PartnerAPIClient,
) -> None:
    await state.clear()

    try:
        partner = await partner_client.fetch_by_id(callback_data.p_id)
    except HTTPStatusError:
        await callback.answer("Ошибка", show_alert=True)
        return

    text, builder = build_partner_detail(partner)
    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(LinkCD.filter(F.action == "link_pick_confirm"))
async def link_pick_confirm(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    partner_client: PartnerAPIClient,
) -> None:
    data = await state.get_data()
    link_ids = data.get("selected_link_ids", [])

    try:
        partner = await partner_client.update(
            callback_data.p_id,
            {"link_ids": link_ids},
        )
    except HTTPStatusError:
        await callback.answer("Не удалось обновить ссылки", show_alert=True)
        return

    await state.clear()

    text, builder = build_partner_detail(partner)
    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer("Ссылки обновлены")
