# packages

from aiogram import Router, F

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message

from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx import HTTPStatusError

# application dependencies

from ..callbacks import NavCD, LinkCD, OfferCD

from ..states import OfferForm

from ..utils import (
    init_form_context,
    edit_menu_message,
    delete_user_message,
)

from ..views.offers import build_offers_list, build_offer_detail

from ..views.links import build_link_detail

from ...infrastructure.clients.api import OfferAPIClient, LinkAPIClient


router = Router()


@router.callback_query(NavCD.filter(F.level == "offers"))
async def show_offers(
    callback: CallbackQuery,
    callback_data: NavCD,
    offer_client: OfferAPIClient,
) -> None:
    try:
        result = await offer_client.fetch_page(page=callback_data.page)
    except HTTPStatusError:
        await callback.answer("Ошибка загрузки офферов", show_alert=True)
        return

    text, builder = build_offers_list(
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

    text, builder = build_offer_detail(
        offer,
        p_id=callback_data.p_id,
        l_id=callback_data.l_id,
    )

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


async def _start_offer_create(
    callback: CallbackQuery,
    state: FSMContext,
    p_id: int,
    l_id: int,
) -> None:
    await init_form_context(
        state,
        callback,
        p_id=p_id,
        l_id=l_id,
    )

    if l_id:
        cancel_data = LinkCD(action="view", p_id=p_id, l_id=l_id)
    else:
        cancel_data = NavCD(level="offers")

    cancel = InlineKeyboardBuilder()
    cancel.button(text="❌ Отмена", callback_data=cancel_data)
    cancel.adjust(1)

    await edit_menu_message(
        callback.bot,
        state,
        "🎁 <b>Введите название нового оффера:</b>",
        cancel.as_markup(),
    )
    await state.set_state(OfferForm.create_title)


@router.callback_query(OfferCD.filter(F.action == "create"))
async def create_offer_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await _start_offer_create(callback, state, p_id=0, l_id=0)
    await callback.answer()


@router.callback_query(OfferCD.filter(F.action == "create_for_link"))
async def create_offer_for_link_start(
    callback: CallbackQuery,
    callback_data: OfferCD,
    state: FSMContext,
) -> None:
    await _start_offer_create(
        callback,
        state,
        p_id=callback_data.p_id,
        l_id=callback_data.l_id,
    )
    await callback.answer()


@router.message(OfferForm.create_title)
async def create_offer_finish(
    message: Message,
    state: FSMContext,
    offer_client: OfferAPIClient,
    link_client: LinkAPIClient,
) -> None:
    await delete_user_message(message)

    data = await state.get_data()

    try:
        offer = await offer_client.create({"title": message.text.strip()})

        l_id = data.get("l_id", 0)
        if l_id:
            link = await link_client.fetch_by_id(l_id)
            offer_ids = [item.id for item in link.offers]
            await link_client.update(
                l_id,
                {"offer_ids": [*offer_ids, offer.id]},
            )
            link = await link_client.fetch_by_id(l_id)
            text, builder = build_link_detail(link, data.get("p_id", 0))
        else:
            result = await offer_client.fetch_page(page=1)
            text, builder = build_offers_list(
                result.items,
                page=result.page,
                pages=result.pages,
                total=result.total,
            )
    except HTTPStatusError:
        await edit_menu_message(
            message.bot,
            state,
            "❌ Не удалось создать оффер",
        )
        await state.clear()
        return

    await edit_menu_message(
        message.bot,
        state,
        text,
        builder.as_markup(),
    )
    await state.clear()


@router.callback_query(OfferCD.filter(F.action == "edit_title"))
async def edit_offer_title_start(
    callback: CallbackQuery,
    callback_data: OfferCD,
    state: FSMContext,
) -> None:
    await init_form_context(
        state,
        callback,
        o_id=callback_data.o_id,
        p_id=callback_data.p_id,
        l_id=callback_data.l_id,
    )

    cancel = InlineKeyboardBuilder()
    cancel.button(
        text="❌ Отмена",
        callback_data=OfferCD(
            action="view",
            p_id=callback_data.p_id,
            l_id=callback_data.l_id,
            o_id=callback_data.o_id,
        ),
    )
    cancel.adjust(1)

    await edit_menu_message(
        callback.bot,
        state,
        "🎁 <b>Введите новое название оффера:</b>",
        cancel.as_markup(),
    )
    await state.set_state(OfferForm.edit_title)
    await callback.answer()


@router.message(OfferForm.edit_title)
async def edit_offer_title_finish(
    message: Message,
    state: FSMContext,
    offer_client: OfferAPIClient,
) -> None:
    await delete_user_message(message)

    data = await state.get_data()

    try:
        offer = await offer_client.update(
            data["o_id"],
            {"title": message.text.strip()},
        )
    except HTTPStatusError:
        await edit_menu_message(
            message.bot,
            state,
            "❌ Не удалось обновить оффер",
        )
        await state.clear()
        return

    text, builder = build_offer_detail(
        offer,
        p_id=data.get("p_id", 0),
        l_id=data.get("l_id", 0),
    )
    await edit_menu_message(
        message.bot,
        state,
        text,
        builder.as_markup(),
    )
    await state.clear()


@router.callback_query(OfferCD.filter(F.action == "delete"))
async def delete_offer(
    callback: CallbackQuery,
    callback_data: OfferCD,
    offer_client: OfferAPIClient,
    link_client: LinkAPIClient,
) -> None:
    try:
        await offer_client.delete(callback_data.o_id)
    except HTTPStatusError:
        await callback.answer("Не удалось удалить оффер", show_alert=True)
        return

    await callback.answer("Оффер удален")

    if callback_data.l_id:
        try:
            link = await link_client.fetch_by_id(callback_data.l_id)
        except HTTPStatusError:
            await callback.message.edit_text("Оффер удален.")
            return

        text, builder = build_link_detail(link, callback_data.p_id)
        await callback.message.edit_text(
            text,
            reply_markup=builder.as_markup(),
            parse_mode="HTML",
        )
    else:
        await show_offers(callback, NavCD(level="offers"), offer_client)
