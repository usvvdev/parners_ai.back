# packages

from aiogram.filters.callback_data import CallbackData


class OfferCD(
    CallbackData,
    prefix="offer",
):
    action: str
    p_id: int
    l_id: int
    o_id: int
    page: int = 1
