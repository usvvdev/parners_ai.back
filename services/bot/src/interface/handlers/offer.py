# packages

from aiogram import Router, F

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message

from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx import HTTPStatusError

# application dependencies

from ..callbacks import NavCD, LinkCD, OfferCD

from ..states import OfferForm

from ..utils import safe

from ...infrastructure.clients.api import OfferAPIClient, LinkAPIClient


router = Router()


@router.callback_query(NavCD.filter(F.level == "offers"))
async def show_offers(
    callback: CallbackQuery,
    offer_client: OfferAPIClient,
) -> None:
    try:
        offers = await offer_client.fetch_all()
    except HTTPStatusError:
        await callback.answer("Ошибка загрузки офферов", show_alert=True)
        return

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

    builder.adjust(1)

    await callback.message.edit_text(
        "🎁 <b>Список офферов:</b>"
        if offers
        else "🎁 <b>Офферов пока нет.</b>",
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

    builder = InlineKeyboardBuilder()

    builder.button(
        text="✏️ Изменить название",
        callback_data=OfferCD(
            action="edit_title",
            p_id=callback_data.p_id,
            l_id=callback_data.l_id,
            o_id=offer.id,
        ),
    )
    builder.button(
        text="🗑 Удалить оффер",
        callback_data=OfferCD(
            action="delete",
            p_id=callback_data.p_id,
            l_id=callback_data.l_id,
            o_id=offer.id,
        ),
    )
    builder.button(
        text="🔙 Назад к ссылке" if callback_data.l_id else "🔙 Назад к офферам",
        callback_data=(
            LinkCD(
                action="view",
                p_id=callback_data.p_id,
                l_id=callback_data.l_id,
            )
            if callback_data.l_id
            else NavCD(level="offers")
        ),
    )
    builder.adjust(1)

    await callback.message.edit_text(
        f"🎁 <b>Оффер:</b> {safe(offer.title)}\n"
        f"🆔 <b>ID:</b> {offer.id}",
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(OfferCD.filter(F.action == "create"))
async def create_offer_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(OfferForm.create_title)
    await callback.message.answer("Введите название нового оффера:")
    await callback.answer()


@router.callback_query(OfferCD.filter(F.action == "create_for_link"))
async def create_offer_for_link_start(
    callback: CallbackQuery,
    callback_data: OfferCD,
    state: FSMContext,
) -> None:
    await state.update_data(p_id=callback_data.p_id, l_id=callback_data.l_id)
    await state.set_state(OfferForm.create_title)
    await callback.message.answer("Введите название нового оффера:")
    await callback.answer()


@router.message(OfferForm.create_title)
async def create_offer_finish(
    message: Message,
    state: FSMContext,
    offer_client: OfferAPIClient,
    link_client: LinkAPIClient,
) -> None:
    data = await state.get_data()
    await state.clear()

    try:
        offer = await offer_client.create({"title": message.text.strip()})

        l_id = data.get("l_id")
        if l_id:
            link = await link_client.fetch_by_id(l_id)
            offer_ids = [item.id for item in link.offers]
            await link_client.update(
                l_id,
                {"offer_ids": [*offer_ids, offer.id]},
            )
    except HTTPStatusError:
        await message.answer("Не удалось создать или привязать оффер")
        return

    await message.answer(f"Оффер создан: <b>{safe(offer.title)}</b>", parse_mode="HTML")


@router.callback_query(OfferCD.filter(F.action == "edit_title"))
async def edit_offer_title_start(
    callback: CallbackQuery,
    callback_data: OfferCD,
    state: FSMContext,
) -> None:
    await state.update_data(o_id=callback_data.o_id)
    await state.set_state(OfferForm.edit_title)
    await callback.message.answer("Введите новое название оффера:")
    await callback.answer()


@router.message(OfferForm.edit_title)
async def edit_offer_title_finish(
    message: Message,
    state: FSMContext,
    offer_client: OfferAPIClient,
) -> None:
    data = await state.get_data()
    await state.clear()

    try:
        await offer_client.update(data["o_id"], {"title": message.text.strip()})
    except HTTPStatusError:
        await message.answer("Не удалось обновить оффер")
        return

    await message.answer("Оффер обновлен")


@router.callback_query(OfferCD.filter(F.action == "delete"))
async def delete_offer(
    callback: CallbackQuery,
    callback_data: OfferCD,
    offer_client: OfferAPIClient,
) -> None:
    try:
        await offer_client.delete(callback_data.o_id)
    except HTTPStatusError:
        await callback.answer("Не удалось удалить оффер", show_alert=True)
        return

    await callback.answer("Оффер удален")
    if callback_data.l_id:
        await callback.message.edit_text("Оффер удален. Вернитесь к ссылке из меню.")
    else:
        await show_offers(callback, offer_client)
