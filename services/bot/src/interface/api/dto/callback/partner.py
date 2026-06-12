# packages

from aiogram.filters.callback_data import CallbackData


class PartnerCD(
    CallbackData,
    prefix="partner",
):
    action: str
    p_id: int
    is_tracking: int = 0
    is_selected: int = 0
    page: int = 1
