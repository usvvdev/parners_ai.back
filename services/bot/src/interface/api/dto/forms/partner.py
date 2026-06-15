# packages

from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class PartnerForm(StatesGroup):
    create_wmid = State()
    select_utm_source = State()
    select_links = State()
    edit_wmid = State()
    edit_utm_source = State()
