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

from httpx import HTTPStatusError

# application depencies

from ..dto.callback import (
    NavigationCD,
    LinkCD,
    OfferCD,
)

from ..dto.forms import LinkForm

from ..views import (
    LinkView,
    PartnerView,
)

from ..views.base import build_form_prompt

from ...services import (
    LinkService,
    PartnerService,
)

from ....domain.types.enums.actions import (
    LinkAction,
    OfferAction,
)

from ....domain.types.enums.common import (
    NavLevel,
    PickMode,
)

from ....domain.types._types import (
    InsertLink,
    FetchPartners,
)

from ....infrastructure.utils.decorators import (
    handle_http_error,
    handle_form_submit,
)

from ....infrastructure.utils.functions import (
    init_form_context,
    edit_menu_message,
    delete_user_message,
    render_callback,
)


link_router = Router()


async def _render_offer_picker(
    bot,
    state: FSMContext,
    link_service: LinkService,
) -> None:
    data = await state.get_data()
    selected_ids = set(data.get("selected_offer_ids", []))

    offers = await link_service.fetch_all_offers()
    text, builder = LinkView.offer_picker(
        offers,
        selected_ids,
        p_id=data.get("p_id", 0),
        l_id=data.get("l_id", 0),
        mode=data.get("offer_pick_mode", PickMode.CREATE),
    )

    await edit_menu_message(bot, state, text, builder.as_markup())


@link_router.callback_query(NavigationCD.filter(F.level == NavLevel.LINKS))
@handle_http_error("Ошибка загрузки ссылок")
async def link_list(
    callback: CallbackQuery,
    callback_data: NavigationCD,
    link_service: LinkService,
) -> None:
    data = await link_service.fetch(page=callback_data.page)
    text, builder = LinkView.list(data)
    await render_callback(callback, text, builder)


@link_router.callback_query(LinkCD.filter(F.action == LinkAction.VIEW))
@handle_http_error("Ссылка не найдена")
async def link_detail(
    callback: CallbackQuery,
    callback_data: LinkCD,
    link_service: LinkService,
) -> None:
    link = await link_service.fetch_by_id(callback_data.l_id)
    text, builder = LinkView.detail(link, p_id=callback_data.p_id)
    await render_callback(callback, text, builder)


@link_router.callback_query(LinkCD.filter(F.action == LinkAction.TOGGLE))
@handle_http_error("Ошибка обновления статуса")
async def link_toggle(
    callback: CallbackQuery,
    callback_data: LinkCD,
    link_service: LinkService,
) -> None:
    link, new_status = await link_service.toggle(callback_data.l_id)
    text, builder = LinkView.detail(link, p_id=callback_data.p_id)

    answer = "активирована" if new_status else "деактивирована"
    await render_callback(callback, text, builder, answer=f"Ссылка {answer}")


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
        offer_pick_mode=PickMode.CREATE,
        selected_offer_ids=[],
    )

    text, markup = build_form_prompt(
        "🔗 <b>Введите URL новой ссылки:</b>",
        LinkCD(action=LinkAction.CREATE_CANCEL, p_id=p_id, l_id=0),
    )
    await edit_menu_message(callback.bot, state, text, markup)
    await state.set_state(LinkForm.create_url)


@link_router.callback_query(LinkCD.filter(F.action == LinkAction.CREATE))
async def create_link_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await _start_link_create(callback, state, p_id=0)
    await callback.answer()


@link_router.callback_query(LinkCD.filter(F.action == LinkAction.CREATE_FOR_PARTNER))
async def create_partner_link_start(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
) -> None:
    await _start_link_create(callback, state, p_id=callback_data.p_id)
    await callback.answer()


@link_router.callback_query(LinkCD.filter(F.action == LinkAction.CREATE_CANCEL))
@handle_http_error("Ошибка")
async def create_link_cancel(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    link_service: LinkService,
    partner_service: PartnerService,
) -> None:
    await state.clear()

    if callback_data.p_id:
        partner = await partner_service.fetch_by_id(callback_data.p_id)
        text, builder = PartnerView.detail(partner)
    else:
        data = await link_service.fetch(page=1)
        text, builder = LinkView.list(data)

    await render_callback(callback, text, builder)


@link_router.message(LinkForm.create_url)
async def create_link_url(
    message: Message,
    state: FSMContext,
    link_service: LinkService,
) -> None:
    await delete_user_message(message)
    await state.update_data(
        link=message.text.strip(),
        selected_offer_ids=[],
    )
    await state.set_state(LinkForm.select_offers)

    try:
        await _render_offer_picker(message.bot, state, link_service)
    except HTTPStatusError:
        await edit_menu_message(
            message.bot,
            state,
            "❌ Ошибка загрузки офферов",
        )
        await state.clear()


@link_router.callback_query(OfferCD.filter(F.action == OfferAction.PICK_TOGGLE))
async def pick_offer_toggle(
    callback: CallbackQuery,
    callback_data: OfferCD,
    state: FSMContext,
    link_service: LinkService,
) -> None:
    data = await state.get_data()
    selected_ids = set(data.get("selected_offer_ids", []))

    if callback_data.o_id in selected_ids:
        selected_ids.remove(callback_data.o_id)
    else:
        selected_ids.add(callback_data.o_id)

    await state.update_data(selected_offer_ids=list(selected_ids))
    await _render_offer_picker(callback.bot, state, link_service)
    await callback.answer()


@link_router.callback_query(OfferCD.filter(F.action == OfferAction.PICK_CANCEL))
@handle_http_error("Ошибка")
async def pick_offer_cancel(
    callback: CallbackQuery,
    callback_data: OfferCD,
    state: FSMContext,
    link_service: LinkService,
    partner_service: PartnerService,
) -> None:
    data = await state.get_data()
    mode = data.get("offer_pick_mode", PickMode.CREATE)
    await state.clear()

    if mode == PickMode.EDIT and callback_data.l_id:
        link = await link_service.fetch_by_id(callback_data.l_id)
        text, builder = LinkView.detail(link, p_id=callback_data.p_id)
    elif callback_data.p_id:
        partner = await partner_service.fetch_by_id(callback_data.p_id)
        text, builder = PartnerView.detail(partner)
    else:
        data = await link_service.fetch(page=1)
        text, builder = LinkView.list(data)

    await render_callback(callback, text, builder)


@link_router.callback_query(OfferCD.filter(F.action == OfferAction.PICK_CONFIRM))
@handle_http_error("Не удалось сохранить ссылку")
async def pick_offer_confirm(
    callback: CallbackQuery,
    state: FSMContext,
    link_service: LinkService,
) -> None:
    data = await state.get_data()
    mode = data.get("offer_pick_mode", PickMode.CREATE)
    offer_ids = data.get("selected_offer_ids", [])

    if mode == PickMode.CREATE:
        result = await link_service.create_with_offers(
            InsertLink(link=data["link"], offer_ids=offer_ids),
            p_id=data.get("p_id", 0),
        )
    else:
        result = await link_service.update_offers(data["l_id"], offer_ids)

    await state.clear()

    if isinstance(result, FetchPartners):
        text, builder = PartnerView.detail(result)
    else:
        text, builder = LinkView.detail(result)

    await render_callback(callback, text, builder, answer="Сохранено")


@link_router.callback_query(LinkCD.filter(F.action == LinkAction.EDIT_URL))
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

    text, markup = build_form_prompt(
        "🔗 <b>Введите новый URL ссылки:</b>",
        LinkCD(
            action=LinkAction.VIEW,
            p_id=callback_data.p_id,
            l_id=callback_data.l_id,
        ),
    )
    await edit_menu_message(callback.bot, state, text, markup)
    await state.set_state(LinkForm.edit_url)
    await callback.answer()


@link_router.message(LinkForm.edit_url)
@handle_form_submit("❌ Не удалось обновить ссылку")
async def edit_link_url_finish(
    message: Message,
    state: FSMContext,
    link_service: LinkService,
) -> tuple[str, ...]:
    data = await state.get_data()

    link = await link_service.update_url(
        data["l_id"],
        message.text.strip(),
    )

    text, builder = LinkView.detail(link, p_id=data.get("p_id", 0))

    return text, builder.as_markup()


@link_router.callback_query(LinkCD.filter(F.action == LinkAction.EDIT_OFFERS))
@handle_http_error("Ссылка не найдена")
async def edit_link_offers_start(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    link_service: LinkService,
) -> None:
    selected_offer_ids = await link_service.fetch_offer_ids(callback_data.l_id)

    await init_form_context(
        state,
        callback,
        l_id=callback_data.l_id,
        p_id=callback_data.p_id,
        offer_pick_mode=PickMode.EDIT,
        selected_offer_ids=selected_offer_ids,
    )
    await state.set_state(LinkForm.select_offers)
    await _render_offer_picker(callback.bot, state, link_service)
    await callback.answer()


@link_router.callback_query(LinkCD.filter(F.action == LinkAction.DELETE))
@handle_http_error("Не удалось удалить ссылку")
async def delete_link(
    callback: CallbackQuery,
    callback_data: LinkCD,
    link_service: LinkService,
    partner_service: PartnerService,
) -> None:
    await link_service.delete(callback_data.l_id)

    if callback_data.p_id:
        partner = await partner_service.fetch_by_id(callback_data.p_id)
        text, builder = PartnerView.detail(partner)
    else:
        data = await link_service.fetch(page=1)
        text, builder = LinkView.list(data)

    await render_callback(callback, text, builder, answer="Ссылка удалена")
