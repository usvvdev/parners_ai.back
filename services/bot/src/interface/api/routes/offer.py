# packages

from aiogram import (
    Router,
    F,
)

from aiogram.fsm.context import FSMContext

from aiogram.types import (
    CallbackQuery,
    Message,
)

# application depencies

from ..dto.callback import (
    NavigationCD,
    LinkCD,
    OfferCD,
)

from ..dto.forms import OfferForm

from ..views import (
    OfferView,
    LinkView,
)

from ...services import OfferService

from ..views.base import build_form_prompt

from ....domain.types.enums.actions import (
    LinkAction,
    OfferAction,
)

from ....domain.types.enums.common import NavLevel

from libs.infrastructure.clients.http.schemas import (
    InsertOffer,
    FetchLink,
)

from httpx import HTTPStatusError

from ....infrastructure.utils.decorators import handle_http_error

from ....infrastructure.utils.functions import (
    init_form_context,
    edit_menu_message,
    delete_user_message,
    render_callback,
    clear_state_keep_filters,
)


offer_router = Router()


@offer_router.callback_query(NavigationCD.filter(F.level == NavLevel.OFFERS))
@handle_http_error("Ошибка загрузки офферов")
async def offer_list(
    callback: CallbackQuery,
    callback_data: NavigationCD,
    offer_service: OfferService,
) -> None:
    data = await offer_service.fetch(page=callback_data.page)
    text, builder = OfferView.list(data)
    await render_callback(callback, text, builder)


@offer_router.callback_query(OfferCD.filter(F.action == OfferAction.VIEW))
@handle_http_error("Оффер не найден")
async def offer_detail(
    callback: CallbackQuery,
    callback_data: OfferCD,
    offer_service: OfferService,
) -> None:
    offer = await offer_service.fetch_by_id(callback_data.o_id)
    text, builder = OfferView.detail(
        offer,
        p_id=callback_data.p_id,
        l_id=callback_data.l_id,
    )
    await render_callback(callback, text, builder)


async def _start_offer_create(
    callback: CallbackQuery,
    state: FSMContext,
    p_id: int,
    l_id: int,
) -> None:
    await init_form_context(state, callback, p_id=p_id, l_id=l_id)

    cancel_data = (
        LinkCD(action=LinkAction.VIEW, p_id=p_id, l_id=l_id)
        if l_id
        else NavigationCD(level=NavLevel.OFFERS)
    )
    text, markup = build_form_prompt(
        "📋 <b>Введите название нового оффера:</b>",
        cancel_data,
    )
    await edit_menu_message(callback.bot, state, text, markup)
    await state.set_state(OfferForm.create_title)


@offer_router.callback_query(OfferCD.filter(F.action == OfferAction.CREATE))
async def create_offer_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await _start_offer_create(callback, state, p_id=0, l_id=0)
    await callback.answer()


@offer_router.callback_query(OfferCD.filter(F.action == OfferAction.CREATE_FOR_LINK))
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


@offer_router.message(OfferForm.create_title)
async def create_offer_title(
    message: Message,
    state: FSMContext,
) -> None:
    title = message.text.strip()

    if not title:
        await message.answer("❌ Название не может быть пустым.")
        return

    await delete_user_message(message)

    data = await state.get_data()
    await state.update_data(title=title)

    cancel_data = (
        LinkCD(
            action=LinkAction.VIEW, p_id=data.get("p_id", 0), l_id=data.get("l_id", 0)
        )
        if data.get("l_id")
        else NavigationCD(level=NavLevel.OFFERS)
    )
    text, markup = build_form_prompt(
        "🏷 <b>Введите символ оффера</b> (до 8 символов, например: З, Б, К):",
        cancel_data,
    )
    await edit_menu_message(message.bot, state, text, markup)
    await state.set_state(OfferForm.create_symbol)


@offer_router.message(OfferForm.create_symbol)
async def create_offer_finish(
    message: Message,
    state: FSMContext,
    offer_service: OfferService,
) -> None:
    symbol = message.text.strip()

    if not symbol or len(symbol) > 8:
        await message.answer("❌ Символ должен быть от 1 до 8 символов.")
        return

    await delete_user_message(message)

    data = await state.get_data()

    try:
        result = await offer_service.create(
            InsertOffer(
                title=data["title"],
                symbol=symbol,
            ),
            l_id=data.get("l_id", 0),
        )
    except HTTPStatusError:
        await edit_menu_message(
            message.bot,
            state,
            "❌ Не удалось создать оффер",
        )
        await clear_state_keep_filters(state)
        return

    if isinstance(result, FetchLink):
        text, builder = LinkView.detail(result, p_id=data.get("p_id", 0))
    else:
        page_data = await offer_service.fetch(page=1)
        text, builder = OfferView.list(page_data)

    await edit_menu_message(
        message.bot,
        state,
        text,
        builder.as_markup(),
    )
    await clear_state_keep_filters(state)


@offer_router.callback_query(OfferCD.filter(F.action == OfferAction.DELETE))
@handle_http_error("Не удалось удалить оффер")
async def delete_offer(
    callback: CallbackQuery,
    callback_data: OfferCD,
    offer_service: OfferService,
) -> None:
    await offer_service.delete(callback_data.o_id)

    if callback_data.l_id:
        link = await offer_service.fetch_link(callback_data.l_id)
        text, builder = LinkView.detail(link, p_id=callback_data.p_id)
    else:
        data = await offer_service.fetch(page=1)
        text, builder = OfferView.list(data)

    await render_callback(callback, text, builder, answer="Оффер удален")
