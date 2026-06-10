# packages

from aiogram import Router, F

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message

from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx import HTTPStatusError

# application dependencies

from ..callbacks import NavCD, LinkCD, OfferCD

from ..states import LinkForm

from ..utils import (
    init_form_context,
    edit_menu_message,
    delete_user_message,
)

from ..views.links import (
    build_links_list,
    build_link_detail,
    build_offer_picker,
)

from ..views.partners import build_partner_detail

from ...infrastructure.clients.api import (
    LinkAPIClient,
    PartnerAPIClient,
    OfferAPIClient,
)


router = Router()


async def _render_offer_picker(
    bot,
    state: FSMContext,
    offer_client: OfferAPIClient,
) -> None:
    data = await state.get_data()
    offers = await offer_client.fetch_all()
    selected_ids = set(data.get("selected_offer_ids", []))

    text, builder = build_offer_picker(
        offers,
        selected_ids,
        p_id=data.get("p_id", 0),
        l_id=data.get("l_id", 0),
        mode=data.get("offer_pick_mode", "create"),
    )

    await edit_menu_message(
        bot,
        state,
        text,
        builder.as_markup(),
    )


@router.callback_query(NavCD.filter(F.level == "links"))
async def show_links(
    callback: CallbackQuery,
    link_client: LinkAPIClient,
) -> None:
    try:
        links = await link_client.fetch_all()
    except HTTPStatusError:
        await callback.answer("Ошибка загрузки ссылок", show_alert=True)
        return

    text, builder = build_links_list(links)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


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

    text, builder = build_link_detail(link, callback_data.p_id)

    await callback.message.edit_text(
        text,
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
        link = await link_client.fetch_by_id(callback_data.l_id)
    except HTTPStatusError:
        await callback.answer("Ошибка обновления статуса", show_alert=True)
        return

    status_text = "активирована" if new_status else "деактивирована"
    await callback.answer(f"Ссылка {status_text}")

    text, builder = build_link_detail(link, callback_data.p_id)
    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )


async def _start_link_create(
    callback: CallbackQuery,
    state: FSMContext,
    p_id: int,
) -> None:
    await init_form_context(
        state,
        callback,
        p_id=p_id,
        l_id=0,
        offer_pick_mode="create",
        selected_offer_ids=[],
    )

    cancel = InlineKeyboardBuilder()
    cancel.button(
        text="❌ Отмена",
        callback_data=LinkCD(action="create_cancel", p_id=p_id, l_id=0),
    )
    cancel.adjust(1)

    await edit_menu_message(
        callback.bot,
        state,
        "🔗 <b>Введите URL новой ссылки:</b>",
        cancel.as_markup(),
    )
    await state.set_state(LinkForm.create_url)


@router.callback_query(LinkCD.filter(F.action == "create"))
async def create_link_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await _start_link_create(callback, state, p_id=0)
    await callback.answer()


@router.callback_query(LinkCD.filter(F.action == "create_for_partner"))
async def create_partner_link_start(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
) -> None:
    await _start_link_create(callback, state, p_id=callback_data.p_id)
    await callback.answer()


@router.callback_query(LinkCD.filter(F.action == "create_cancel"))
async def create_link_cancel(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    link_client: LinkAPIClient,
    partner_client: PartnerAPIClient,
) -> None:
    await state.clear()

    if callback_data.p_id:
        try:
            partner = await partner_client.fetch_by_id(callback_data.p_id)
        except HTTPStatusError:
            await callback.answer("Ошибка", show_alert=True)
            return

        text, builder = build_partner_detail(partner)
    else:
        try:
            links = await link_client.fetch_all()
        except HTTPStatusError:
            await callback.answer("Ошибка", show_alert=True)
            return

        text, builder = build_links_list(links)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(LinkForm.create_url)
async def create_link_url(
    message: Message,
    state: FSMContext,
    offer_client: OfferAPIClient,
) -> None:
    await delete_user_message(message)
    await state.update_data(
        link=message.text.strip(),
        selected_offer_ids=[],
    )
    await state.set_state(LinkForm.select_offers)
    await _render_offer_picker(message.bot, state, offer_client)


@router.callback_query(OfferCD.filter(F.action == "pick_toggle"))
async def pick_offer_toggle(
    callback: CallbackQuery,
    callback_data: OfferCD,
    state: FSMContext,
    offer_client: OfferAPIClient,
) -> None:
    data = await state.get_data()
    selected_ids = set(data.get("selected_offer_ids", []))

    if callback_data.o_id in selected_ids:
        selected_ids.remove(callback_data.o_id)
    else:
        selected_ids.add(callback_data.o_id)

    await state.update_data(selected_offer_ids=list(selected_ids))
    await _render_offer_picker(callback.bot, state, offer_client)
    await callback.answer()


@router.callback_query(OfferCD.filter(F.action == "pick_cancel"))
async def pick_offer_cancel(
    callback: CallbackQuery,
    callback_data: OfferCD,
    state: FSMContext,
    link_client: LinkAPIClient,
    partner_client: PartnerAPIClient,
) -> None:
    data = await state.get_data()
    mode = data.get("offer_pick_mode", "create")
    await state.clear()

    if mode == "edit" and callback_data.l_id:
        try:
            link = await link_client.fetch_by_id(callback_data.l_id)
        except HTTPStatusError:
            await callback.answer("Ошибка", show_alert=True)
            return

        text, builder = build_link_detail(link, callback_data.p_id)
    elif callback_data.p_id:
        try:
            partner = await partner_client.fetch_by_id(callback_data.p_id)
        except HTTPStatusError:
            await callback.answer("Ошибка", show_alert=True)
            return

        text, builder = build_partner_detail(partner)
    else:
        try:
            links = await link_client.fetch_all()
        except HTTPStatusError:
            await callback.answer("Ошибка", show_alert=True)
            return

        text, builder = build_links_list(links)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(OfferCD.filter(F.action == "pick_confirm"))
async def pick_offer_confirm(
    callback: CallbackQuery,
    callback_data: OfferCD,
    state: FSMContext,
    link_client: LinkAPIClient,
    partner_client: PartnerAPIClient,
) -> None:
    data = await state.get_data()
    mode = data.get("offer_pick_mode", "create")
    offer_ids = data.get("selected_offer_ids", [])

    try:
        if mode == "create":
            link = await link_client.create(
                {
                    "link": data["link"],
                    "is_active": True,
                    "offer_ids": offer_ids,
                }
            )

            p_id = data.get("p_id", 0)
            if p_id:
                partner = await partner_client.fetch_by_id(p_id)
                link_ids = [item.id for item in partner.links]
                partner = await partner_client.update(
                    p_id,
                    {"link_ids": [*link_ids, link.id]},
                )
                text, builder = build_partner_detail(partner)
            else:
                links = await link_client.fetch_all()
                text, builder = build_links_list(links)
        else:
            await link_client.update(
                data["l_id"],
                {"offer_ids": offer_ids},
            )
            link = await link_client.fetch_by_id(data["l_id"])
            text, builder = build_link_detail(link, data.get("p_id", 0))
    except HTTPStatusError:
        await callback.answer("Не удалось сохранить ссылку", show_alert=True)
        return

    await state.clear()
    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer("Сохранено")


@router.callback_query(LinkCD.filter(F.action == "edit_url"))
async def edit_link_url_start(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
) -> None:
    await init_form_context(
        state,
        callback,
        l_id=callback_data.l_id,
        p_id=callback_data.p_id,
    )

    cancel = InlineKeyboardBuilder()
    cancel.button(
        text="❌ Отмена",
        callback_data=LinkCD(
            action="view",
            p_id=callback_data.p_id,
            l_id=callback_data.l_id,
        ),
    )
    cancel.adjust(1)

    await edit_menu_message(
        callback.bot,
        state,
        "🔗 <b>Введите новый URL ссылки:</b>",
        cancel.as_markup(),
    )
    await state.set_state(LinkForm.edit_url)
    await callback.answer()


@router.message(LinkForm.edit_url)
async def edit_link_url_finish(
    message: Message,
    state: FSMContext,
    link_client: LinkAPIClient,
) -> None:
    await delete_user_message(message)

    data = await state.get_data()

    try:
        await link_client.update(data["l_id"], {"link": message.text.strip()})
        link = await link_client.fetch_by_id(data["l_id"])
    except HTTPStatusError:
        await edit_menu_message(
            message.bot,
            state,
            "❌ Не удалось обновить ссылку",
        )
        await state.clear()
        return

    text, builder = build_link_detail(link, data.get("p_id", 0))
    await edit_menu_message(
        message.bot,
        state,
        text,
        builder.as_markup(),
    )
    await state.clear()


@router.callback_query(LinkCD.filter(F.action == "edit_offers"))
async def edit_link_offers_start(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    link_client: LinkAPIClient,
    offer_client: OfferAPIClient,
) -> None:
    try:
        link = await link_client.fetch_by_id(callback_data.l_id)
    except HTTPStatusError:
        await callback.answer("Ссылка не найдена", show_alert=True)
        return

    await init_form_context(
        state,
        callback,
        l_id=callback_data.l_id,
        p_id=callback_data.p_id,
        offer_pick_mode="edit",
        selected_offer_ids=[offer.id for offer in link.offers],
    )
    await state.set_state(LinkForm.select_offers)
    await _render_offer_picker(callback.bot, state, offer_client)
    await callback.answer()


@router.callback_query(LinkCD.filter(F.action == "delete"))
async def delete_link(
    callback: CallbackQuery,
    callback_data: LinkCD,
    link_client: LinkAPIClient,
    partner_client: PartnerAPIClient,
) -> None:
    try:
        await link_client.delete(callback_data.l_id)
    except HTTPStatusError:
        await callback.answer("Не удалось удалить ссылку", show_alert=True)
        return

    await callback.answer("Ссылка удалена")

    if callback_data.p_id:
        try:
            partner = await partner_client.fetch_by_id(callback_data.p_id)
        except HTTPStatusError:
            await callback.message.edit_text("Ссылка удалена.")
            return

        text, builder = build_partner_detail(partner)
        await callback.message.edit_text(
            text,
            reply_markup=builder.as_markup(),
            parse_mode="HTML",
        )
    else:
        await show_links(callback, link_client)
