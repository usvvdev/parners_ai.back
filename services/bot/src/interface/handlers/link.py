# packages

from aiogram import Router, F

from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message

from aiogram.utils.keyboard import InlineKeyboardBuilder

from httpx import HTTPStatusError

# application dependencies

from ..callbacks import NavCD, PartnerCD, LinkCD, OfferCD

from ..states import LinkForm

from ..utils import safe, short_url, parse_ids

from ...infrastructure.clients.api import LinkAPIClient


router = Router()


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

    builder = InlineKeyboardBuilder()
    builder.button(
        text="➕ Добавить ссылку",
        callback_data=LinkCD(action="create", p_id=0, l_id=0),
    )

    for link in links:
        builder.button(
            text=f"🔗 {short_url(link.link)}",
            callback_data=LinkCD(action="view", p_id=0, l_id=link.id),
        )

    builder.adjust(1)

    await callback.message.edit_text(
        "🔗 <b>Список ссылок:</b>"
        if links
        else "🔗 <b>Ссылок пока нет.</b>",
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
    builder.button(
        text="✏️ Изменить URL",
        callback_data=LinkCD(
            action="edit_url",
            p_id=callback_data.p_id,
            l_id=link.id,
        ),
    )
    builder.button(
        text="✏️ Изменить офферы",
        callback_data=LinkCD(
            action="edit_offers",
            p_id=callback_data.p_id,
            l_id=link.id,
        ),
    )
    builder.button(
        text="➕ Создать оффер",
        callback_data=OfferCD(
            action="create_for_link",
            p_id=callback_data.p_id,
            l_id=link.id,
            o_id=0,
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
        text="🗑 Удалить ссылку",
        callback_data=LinkCD(
            action="delete",
            p_id=callback_data.p_id,
            l_id=link.id,
        ),
    )
    if callback_data.p_id:
        builder.button(
            text="🔙 Назад к партнеру",
            callback_data=PartnerCD(action="view", p_id=callback_data.p_id),
        )
    else:
        builder.button(
            text="🔙 Назад к ссылкам",
            callback_data=NavCD(level="links"),
        )
    builder.adjust(1)

    await callback.message.edit_text(
        f"🔗 <b>Ссылка:</b> {safe(short_url(link.link, limit=80))}\n"
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


@router.callback_query(LinkCD.filter(F.action == "create"))
async def create_link_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(LinkForm.create_url)
    await callback.message.answer("Введите URL новой ссылки:")
    await callback.answer()


@router.callback_query(LinkCD.filter(F.action == "edit_url"))
async def edit_link_url_start(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
) -> None:
    await state.update_data(l_id=callback_data.l_id)
    await state.set_state(LinkForm.edit_url)
    await callback.message.answer("Введите новый URL ссылки:")
    await callback.answer()


@router.message(LinkForm.edit_url)
async def edit_link_url_finish(
    message: Message,
    state: FSMContext,
    link_client: LinkAPIClient,
) -> None:
    data = await state.get_data()
    await state.clear()

    try:
        await link_client.update(data["l_id"], {"link": message.text.strip()})
    except HTTPStatusError:
        await message.answer("Не удалось обновить ссылку")
        return

    await message.answer("URL ссылки обновлен")


@router.callback_query(LinkCD.filter(F.action == "edit_offers"))
async def edit_link_offers_start(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
) -> None:
    await state.update_data(l_id=callback_data.l_id)
    await state.set_state(LinkForm.edit_offer_ids)
    await callback.message.answer(
        "Введите новый список ID офферов через запятую или '-' для пустого списка:"
    )
    await callback.answer()


@router.message(LinkForm.edit_offer_ids)
async def edit_link_offers_finish(
    message: Message,
    state: FSMContext,
    link_client: LinkAPIClient,
) -> None:
    data = await state.get_data()
    await state.clear()

    try:
        offer_ids = parse_ids(message.text)
    except ValueError:
        await message.answer("ID офферов должны быть числами через запятую")
        return

    try:
        await link_client.update(data["l_id"], {"offer_ids": offer_ids})
    except HTTPStatusError:
        await message.answer("Не удалось обновить офферы ссылки")
        return

    await message.answer("Офферы ссылки обновлены")


@router.callback_query(LinkCD.filter(F.action == "delete"))
async def delete_link(
    callback: CallbackQuery,
    callback_data: LinkCD,
    link_client: LinkAPIClient,
) -> None:
    try:
        await link_client.delete(callback_data.l_id)
    except HTTPStatusError:
        await callback.answer("Не удалось удалить ссылку", show_alert=True)
        return

    await callback.answer("Ссылка удалена")
    if callback_data.p_id:
        await callback.message.edit_text("Ссылка удалена. Вернитесь к партнеру из меню.")
    else:
        await show_links(callback, link_client)
