# packages

from aiogram.filters.callback_data import CallbackData


class LinkCD(
    CallbackData,
    prefix="link",
):
    action: str
    p_id: int
    l_id: int
    page: int = 1
