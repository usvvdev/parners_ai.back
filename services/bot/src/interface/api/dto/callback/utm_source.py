# packages

from aiogram.filters.callback_data import CallbackData


class UTMSourceCD(
    CallbackData,
    prefix="utm",
):
    action: str
    u_id: int = 0
    page: int = 1
