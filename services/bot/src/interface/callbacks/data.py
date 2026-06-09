# packages

from aiogram.filters.callback_data import CallbackData


class NavCD(CallbackData, prefix="nav"):
    level: str


class PartnerCD(CallbackData, prefix="prt"):
    action: str
    p_id: int


class LinkCD(CallbackData, prefix="lnk"):
    action: str
    p_id: int
    l_id: int


class OfferCD(CallbackData, prefix="off"):
    action: str
    p_id: int
    l_id: int
    o_id: int
