from enum import StrEnum


class UTMSourceAction(StrEnum):
    PICK_SELECT = "pick_select"

    PICK_PAGE = "pick_page"

    PICK_CANCEL = "pick_cancel"

    PICK_CONFIRM = "pick_confirm"
