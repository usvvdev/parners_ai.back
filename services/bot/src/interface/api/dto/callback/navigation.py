# packages

from aiogram.filters.callback_data import CallbackData

from .....core.constants import FILTER_ALL


class NavigationCD(
    CallbackData,
    prefix="nav",
):
    level: str
    page: int = 1
    fa: int = FILTER_ALL
    ft: int = FILTER_ALL
    fs: int = FILTER_ALL
