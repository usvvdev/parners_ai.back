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
    PartnerCD,
    LinkCD,
)

from ..dto.forms import PartnerForm

from ..views import PartnerView

from ..views.base import build_form_prompt

from ...services import PartnerService

from ....domain.types.enums.actions import (
    PartnerAction,
    LinkAction,
)

from ....domain.types.enums.common import NavLevel

from ....domain.types._types import InsertPartner

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


partner_router = Router()


async def _render_link_picker(
    bot,
    state: FSMContext,
    partner_service: PartnerService,
    *,
    page: int | None = None,
) -> None:
    data = await state.get_data()
    current_page = page if page is not None else data.get("picker_page", 1)
    selected_ids = set(data.get("selected_link_ids", []))

    await state.update_data(picker_page=current_page)

    links = await partner_service.fetch_links(page=current_page)
    text, builder = PartnerView.link_picker(
        links,
        selected_ids,
        p_id=data["p_id"],
    )

    await edit_menu_message(bot, state, text, builder.as_markup())


@partner_router.callback_query(NavigationCD.filter(F.level == NavLevel.PARTNERS))
@handle_http_error("Ошибка загрузки партнеров")
async def partner_list(
    callback: CallbackQuery,
    callback_data: NavigationCD,
    partner_service: PartnerService,
) -> None:
    data = await partner_service.fetch(page=callback_data.page)
    text, builder = PartnerView.list(data)
    await render_callback(callback, text, builder)


@partner_router.callback_query(PartnerCD.filter(F.action == PartnerAction.VIEW))
@handle_http_error("Партнер не найден")
async def partner_detail(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_service: PartnerService,
) -> None:
    partner = await partner_service.fetch_by_id(
        callback_data.p_id,
        page=callback_data.page,
    )
    text, builder = PartnerView.detail(partner)
    await render_callback(callback, text, builder)


@partner_router.callback_query(PartnerCD.filter(F.action == PartnerAction.CREATE))
async def create_partner_start(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await init_form_context(state, callback)

    text, markup = build_form_prompt(
        "🏢 <b>Введите WMID партнера:</b>",
        NavigationCD(level=NavLevel.PARTNERS),
    )
    await edit_menu_message(callback.bot, state, text, markup)
    await state.set_state(PartnerForm.create_wmid)
    await callback.answer()


@partner_router.message(PartnerForm.create_wmid)
async def create_partner_wmid(
    message: Message,
    state: FSMContext,
) -> None:
    await delete_user_message(message)
    await state.update_data(wmid=message.text.strip())

    text, markup = build_form_prompt(
        "🏷 <b>Введите UTM source партнера:</b>",
        NavigationCD(level=NavLevel.PARTNERS),
    )
    await edit_menu_message(message.bot, state, text, markup)
    await state.set_state(PartnerForm.create_utm_source)


@partner_router.message(PartnerForm.create_utm_source)
@handle_form_submit("❌ Не удалось создать партнера")
async def create_partner_finish(
    message: Message,
    state: FSMContext,
    partner_service: PartnerService,
) -> tuple[str, ...]:
    data = await state.get_data()

    result = await partner_service.create(
        InsertPartner(
            wmid=data["wmid"],
            utm_source=message.text.strip(),
        ),
    )

    text, builder = PartnerView.list(result)

    return text, builder.as_markup()


@partner_router.callback_query(PartnerCD.filter(F.action == PartnerAction.SETTINGS))
@handle_http_error("Партнер не найден")
async def partner_settings(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_service: PartnerService,
) -> None:
    partner = await partner_service.fetch_by_id(
        callback_data.p_id,
        page=callback_data.page,
    )
    text, builder = PartnerView.settings(partner)
    await render_callback(callback, text, builder)


@partner_router.callback_query(
    PartnerCD.filter(F.action == PartnerAction.TOGGLE_TRACKING),
)
@handle_http_error("Ошибка обновления трекинга")
async def partner_toggle_tracking(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_service: PartnerService,
) -> None:
    partner = await partner_service.toggle_tracking(
        callback_data.p_id,
        is_tracking=bool(callback_data.is_tracking),
    )
    text, builder = PartnerView.settings(partner)

    status = "включен" if not callback_data.is_tracking else "выключен"
    await render_callback(callback, text, builder, answer=f"Трекинг {status}")


@partner_router.callback_query(
    PartnerCD.filter(F.action == PartnerAction.TOGGLE_SELECTED),
)
@handle_http_error("Ошибка обновления избранного")
async def partner_toggle_selected(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_service: PartnerService,
) -> None:
    partner = await partner_service.toggle_selected(
        callback_data.p_id,
        is_selected=bool(callback_data.is_selected),
    )
    text, builder = PartnerView.settings(partner)

    new_status = not bool(callback_data.is_selected)
    answer = "добавлен в избранное" if new_status else "убран из избранного"
    await render_callback(callback, text, builder, answer=answer)


@partner_router.callback_query(PartnerCD.filter(F.action == PartnerAction.DELETE))
@handle_http_error("Не удалось удалить партнера")
async def delete_partner(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    partner_service: PartnerService,
) -> None:
    await partner_service.delete(callback_data.p_id)
    data = await partner_service.fetch(page=1)
    text, builder = PartnerView.list(data)
    await render_callback(callback, text, builder, answer="Партнер удален")


@partner_router.callback_query(PartnerCD.filter(F.action == PartnerAction.EDIT_LINKS))
@handle_http_error("Партнер не найден")
async def edit_partner_links_start(
    callback: CallbackQuery,
    callback_data: PartnerCD,
    state: FSMContext,
    partner_service: PartnerService,
) -> None:
    selected_link_ids = await partner_service.fetch_link_ids(callback_data.p_id)

    await init_form_context(
        state,
        callback,
        p_id=callback_data.p_id,
        selected_link_ids=selected_link_ids,
        detail_page=callback_data.page,
        picker_page=1,
    )
    await state.set_state(PartnerForm.select_links)
    await _render_link_picker(callback.bot, state, partner_service)
    await callback.answer()


@partner_router.callback_query(LinkCD.filter(F.action == LinkAction.PICK_TOGGLE))
async def link_pick_toggle(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    partner_service: PartnerService,
) -> None:
    data = await state.get_data()
    selected_ids = set(data.get("selected_link_ids", []))

    if callback_data.l_id in selected_ids:
        selected_ids.remove(callback_data.l_id)
    else:
        selected_ids.add(callback_data.l_id)

    await state.update_data(selected_link_ids=list(selected_ids))
    await _render_link_picker(
        callback.bot,
        state,
        partner_service,
        page=callback_data.page,
    )
    await callback.answer()


@partner_router.callback_query(LinkCD.filter(F.action == LinkAction.PICK_PAGE))
async def link_pick_page(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    partner_service: PartnerService,
) -> None:
    await _render_link_picker(
        callback.bot,
        state,
        partner_service,
        page=callback_data.page,
    )
    await callback.answer()


@partner_router.callback_query(LinkCD.filter(F.action == LinkAction.PICK_CANCEL))
@handle_http_error("Ошибка")
async def link_pick_cancel(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    partner_service: PartnerService,
) -> None:
    data = await state.get_data()
    detail_page = data.get("detail_page", callback_data.page)
    await state.clear()

    partner = await partner_service.fetch_by_id(
        callback_data.p_id,
        page=detail_page,
    )
    text, builder = PartnerView.detail(partner)
    await render_callback(callback, text, builder)


@partner_router.callback_query(LinkCD.filter(F.action == LinkAction.PICK_CONFIRM))
@handle_http_error("Не удалось обновить витрины")
async def link_pick_confirm(
    callback: CallbackQuery,
    callback_data: LinkCD,
    state: FSMContext,
    partner_service: PartnerService,
) -> None:
    data = await state.get_data()
    detail_page = data.get("detail_page", 1)

    await partner_service.update_links(
        callback_data.p_id,
        data.get("selected_link_ids", []),
    )

    await state.clear()

    partner = await partner_service.fetch_by_id(
        callback_data.p_id,
        page=detail_page,
    )
    text, builder = PartnerView.detail(partner)
    await render_callback(callback, text, builder, answer="Витрины обновлены")
