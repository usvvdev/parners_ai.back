# packages

from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class LinkForm(StatesGroup):
    create_url = State()
    select_offers = State()
