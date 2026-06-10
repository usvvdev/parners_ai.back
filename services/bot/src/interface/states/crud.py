from aiogram.fsm.state import State, StatesGroup


class PartnerForm(StatesGroup):
    create_wmid = State()
    create_utm_source = State()
    select_links = State()
    edit_wmid = State()
    edit_utm_source = State()


class LinkForm(StatesGroup):
    create_url = State()
    select_offers = State()
    edit_url = State()


class OfferForm(StatesGroup):
    create_title = State()
    edit_title = State()
