from enum import StrEnum


class PartnerAction(StrEnum):
    VIEW = "view"

    CREATE = "create"

    SETTINGS = "settings"

    TOGGLE_TRACKING = "toggle_tracking"

    TOGGLE_SELECTED = "toggle_selected"

    DELETE = "delete"

    EDIT_LINKS = "edit_links"
