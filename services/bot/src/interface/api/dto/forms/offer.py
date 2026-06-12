# packages

from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class OfferForm(StatesGroup):
    create_title = State()
