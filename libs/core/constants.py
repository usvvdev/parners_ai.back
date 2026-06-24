# Configuration variables

BASE_ENCODING = "utf-8"

URL_TEMPLATE = "{driver}://{auth}{host}:{port}{db_path}"

# Variables for the entities

SNAKE_CASE_PATTERN = r"(?<!^)([A-Z][a-z])"

SNAKE_CASE_REPLACEMENT = r"_\1"

# Variables for config

URL_REQUIRED_FIELDS: frozenset[str] = frozenset(
    {"driver", "host", "port"},
)

# Pagination defaults (used by API and bot independently)

DEFAULT_PAGE = 1

DEFAULT_PAGE_SIZE = 6
