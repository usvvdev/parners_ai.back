# packages

from aiogram.filters.callback_data import CallbackData


class NavigationCD(
    CallbackData,
    prefix="navigation",
):
    level: str
    page: int = 1
