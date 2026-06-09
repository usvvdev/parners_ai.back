from aiogram.fsm.state import State, StatesGroup


class PartnerForm(StatesGroup):
    create_wmid = State()
    create_utm_source = State()
    edit_wmid = State()
    edit_utm_source = State()


class LinkForm(StatesGroup):
    create_url = State()
    create_offer_ids = State()
    edit_url = State()
    edit_offer_ids = State()


class OfferForm(StatesGroup):
    create_title = State()
    edit_title = State()
