from enum import StrEnum


class LinkAction(StrEnum):
    VIEW = "view"

    CREATE = "create"

    CREATE_FOR_PARTNER = "create_for_partner"

    CREATE_CANCEL = "create_cancel"

    TOGGLE = "toggle"

    EDIT_OFFERS = "edit_offers"

    DELETE = "delete"

    PICK_TOGGLE = "link_pick_toggle"

    PICK_PAGE = "link_pick_page"

    PICK_CANCEL = "link_pick_cancel"

    PICK_CONFIRM = "link_pick_confirm"
