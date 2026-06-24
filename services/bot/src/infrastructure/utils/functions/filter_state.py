# packages

from aiogram.fsm.context import FSMContext

# application depencies

from ....interface.api.dto.callback import NavigationCD

from ....core.constants import FILTER_ALL


LINKS_FA_KEY = "links_fa"
PARTNERS_FT_KEY = "partners_ft"
PARTNERS_FS_KEY = "partners_fs"

FILTER_STATE_KEYS = (
    LINKS_FA_KEY,
    PARTNERS_FT_KEY,
    PARTNERS_FS_KEY,
)


async def snapshot_filter_state(
    state: FSMContext,
) -> dict[str, int]:
    fsm = await state.get_data()

    return {
        key: fsm[key]
        for key in FILTER_STATE_KEYS
        if key in fsm
    }


async def restore_filter_state(
    state: FSMContext,
    snapshot: dict[str, int],
) -> None:
    if snapshot:
        await state.update_data(**snapshot)


async def clear_state_keep_filters(
    state: FSMContext,
) -> None:
    snapshot = await snapshot_filter_state(state)
    await state.clear()
    await restore_filter_state(state, snapshot)


async def resolve_link_filter(
    state: FSMContext,
    callback_data: NavigationCD,
) -> int:
    fsm = await state.get_data()

    if callback_data.pr == 0:
        is_active = callback_data.fa
    elif callback_data.page == 1 and callback_data.fa == FILTER_ALL:
        is_active = fsm.get(LINKS_FA_KEY, FILTER_ALL)
    else:
        is_active = callback_data.fa

    await state.update_data(**{LINKS_FA_KEY: is_active})

    return is_active


async def resolve_partner_filters(
    state: FSMContext,
    callback_data: NavigationCD,
) -> tuple[int, int]:
    fsm = await state.get_data()

    if callback_data.pr == 0:
        is_tracking = callback_data.ft
        is_selected = callback_data.fs
    elif (
        callback_data.page == 1
        and callback_data.ft == FILTER_ALL
        and callback_data.fs == FILTER_ALL
    ):
        is_tracking = fsm.get(PARTNERS_FT_KEY, FILTER_ALL)
        is_selected = fsm.get(PARTNERS_FS_KEY, FILTER_ALL)
    else:
        is_tracking = callback_data.ft
        is_selected = callback_data.fs

    await state.update_data(
        **{
            PARTNERS_FT_KEY: is_tracking,
            PARTNERS_FS_KEY: is_selected,
        }
    )

    return is_tracking, is_selected


async def get_link_filter(
    state: FSMContext,
) -> int:
    return (await state.get_data()).get(LINKS_FA_KEY, FILTER_ALL)


async def get_partner_filters(
    state: FSMContext,
) -> tuple[int, int]:
    fsm = await state.get_data()

    return (
        fsm.get(PARTNERS_FT_KEY, FILTER_ALL),
        fsm.get(PARTNERS_FS_KEY, FILTER_ALL),
    )
