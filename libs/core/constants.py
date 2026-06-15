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

# Variables for the system prompt

SYSTEM_PROMPT = """
    Ты анализируешь сайт-витрину МФО/Беттинга. У тебя есть скриншот страницы и её Markdown код.
    Мой список целевых офферов: {target_offers}.

    Твоя задача:
    1. Посмотри на скриншот. Найди на нем все карточки. Ищи логотипы брендов из моего списка (даже если текст не написан, а просто нарисован логотип, например PARI).
    2. Посчитай общее количество карточек.
    3. Найди, на каких позициях (сверху вниз) находятся мои целевые офферы.
    4. Для каждого найденного целевого оффера укажи URL ссылки с карточки (href кнопки/логотипа перехода на оффер). Если ссылки нет — оставь url пустым.

    Markdown код для справки:
    {markdown}
"""

# Pagination defaults (used by API and bot independently)

DEFAULT_PAGE = 1

DEFAULT_PAGE_SIZE = 5
