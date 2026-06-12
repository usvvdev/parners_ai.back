from enum import StrEnum


class OfferAction(StrEnum):
    VIEW = "view"

    CREATE = "create"

    CREATE_FOR_LINK = "create_for_link"

    DELETE = "delete"

    PICK_TOGGLE = "pick_toggle"

    PICK_CANCEL = "pick_cancel"

    PICK_CONFIRM = "pick_confirm"
