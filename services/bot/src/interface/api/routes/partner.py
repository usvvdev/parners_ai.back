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
    PartnerCD,
    LinkCD,
    UTMSourceCD,
)

from ..dto.forms import PartnerForm

from ..views import PartnerView

from ..views.base import build_form_prompt

from ...services import PartnerService

from ....domain.types.enums.actions import (
    PartnerAction,
    LinkAction,
    UTMSourceAction,
)

from ....domain.types.enums.common import NavLevel

from libs.infrastructure.clients.http.schemas import InsertPartner

from ....infrastructure.utils.decorators import (
    handle_http_error,
)

from ....infrastructure.utils.functions import (
    init_form_context,
    edit_menu_message,
    delete_user_message,
    render_callback,
    resolve_partner_filters,
    get_partner_filters,
    clear_state_keep_filters,
)


partner_router = Router()


async def _render_utm_source_picker(
    bot,
    state: FSMContext,
    partner_service: PartnerService,
    *,
    page: int | None = None,
) -> None:
    data = await state.get_data()
    current_page = page if page is not None else data.get("picker_page", 1)
    selected_id = data.get("selected_utm_source_id")

    await state.update_data(picker_page=current_page)

    sources = await partner_service.fetch_utm_sources(page=current_page)
    text, builder = PartnerView.utm_source_picker(
        sources,
        selected_id,
    )

    await edit_menu_message(bot, state, text, builder.as_markup())


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
    state: FSMContext,
) -> None:
    is_tracking, is_selected = await resolve_partner_filters(
        state,
        callback_data,
    )

    data = await partner_service.fetch(
        page=callback_data.page,
        is_tracking=is_tracking,
        is_selected=is_selected,
    )
    text, builder = PartnerView.list(
        data,
        is_tracking=is_tracking,
        is_selected=is_selected,
    )
    await render_callback(callback, text, builder)


@partner_router.callback_query(
    NavigationCD.filter(F.level == NavLevel.PARTNERS_FILTERS)
)
async def partner_filters(
    callback: CallbackQuery,
    callback_data: NavigationCD,
) -> None:
    text, builder = PartnerView.filters(
        is_tracking=callback_data.ft,
        is_selected=callback_data.fs,
        backup_tracking=callback_data.bft,
        backup_selected=callback_data.bfs,
    )
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
    partner_service: PartnerService,
) -> None:
    await delete_user_message(message)
    await state.update_data(
        wmid=message.text.strip(),
        selected_utm_source_id=None,
        picker_page=1,
    )

    await state.set_state(PartnerForm.select_utm_source)

    try:
        await _render_utm_source_picker(message.bot, state, partner_service)
    except HTTPStatusError:
        await edit_menu_message(
            message.bot,
            state,
            "❌ Ошибка загрузки UTM sources",
        )
        await clear_state_keep_filters(state)


@partner_router.callback_query(
    UTMSourceCD.filter(F.action == UTMSourceAction.PICK_SELECT)
)
async def utm_source_pick_select(
    callback: CallbackQuery,
    callback_data: UTMSourceCD,
    state: FSMContext,
    partner_service: PartnerService,
) -> None:
    data = await state.get_data()
    selected_id = data.get("selected_utm_source_id")

    if selected_id == callback_data.u_id:
        await state.update_data(selected_utm_source_id=None)
    else:
        await state.update_data(selected_utm_source_id=callback_data.u_id)

    await _render_utm_source_picker(
        callback.bot,
        state,
        partner_service,
        page=callback_data.page,
    )
    await callback.answer()


@partner_router.callback_query(
    UTMSourceCD.filter(F.action == UTMSourceAction.PICK_PAGE)
)
async def utm_source_pick_page(
    callback: CallbackQuery,
    callback_data: UTMSourceCD,
    state: FSMContext,
    partner_service: PartnerService,
) -> None:
    await _render_utm_source_picker(
        callback.bot,
        state,
        partner_service,
        page=callback_data.page,
    )
    await callback.answer()


@partner_router.callback_query(
    UTMSourceCD.filter(F.action == UTMSourceAction.PICK_CANCEL)
)
@handle_http_error("Ошибка")
async def utm_source_pick_cancel(
    callback: CallbackQuery,
    state: FSMContext,
    partner_service: PartnerService,
) -> None:
    await clear_state_keep_filters(state)
    is_tracking, is_selected = await get_partner_filters(state)
    data = await partner_service.fetch(
        page=1,
        is_tracking=is_tracking,
        is_selected=is_selected,
    )
    text, builder = PartnerView.list(
        data,
        is_tracking=is_tracking,
        is_selected=is_selected,
    )
    await render_callback(callback, text, builder)


@partner_router.callback_query(
    UTMSourceCD.filter(F.action == UTMSourceAction.PICK_CONFIRM)
)
@handle_http_error("❌ Не удалось создать партнера")
async def create_partner_finish(
    callback: CallbackQuery,
    state: FSMContext,
    partner_service: PartnerService,
) -> None:
    data = await state.get_data()
    utm_source_id = data.get("selected_utm_source_id")

    if not utm_source_id:
        await callback.answer("Выберите UTM source", show_alert=True)
        return

    await partner_service.create(
        InsertPartner(
            wmid=data["wmid"],
            utm_source_id=utm_source_id,
        ),
    )

    await clear_state_keep_filters(state)

    is_tracking, is_selected = await get_partner_filters(state)
    result = await partner_service.fetch(
        page=1,
        is_tracking=is_tracking,
        is_selected=is_selected,
    )
    text, builder = PartnerView.list(
        result,
        is_tracking=is_tracking,
        is_selected=is_selected,
    )

    await render_callback(callback, text, builder, answer="Партнер создан")


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
    state: FSMContext,
) -> None:
    await partner_service.delete(callback_data.p_id)
    is_tracking, is_selected = await get_partner_filters(state)
    data = await partner_service.fetch(
        page=1,
        is_tracking=is_tracking,
        is_selected=is_selected,
    )
    text, builder = PartnerView.list(
        data,
        is_tracking=is_tracking,
        is_selected=is_selected,
    )
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
    await clear_state_keep_filters(state)

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

    await clear_state_keep_filters(state)

    partner = await partner_service.fetch_by_id(
        callback_data.p_id,
        page=detail_page,
    )
    text, builder = PartnerView.detail(partner)
    await render_callback(callback, text, builder, answer="Витрины обновлены")
