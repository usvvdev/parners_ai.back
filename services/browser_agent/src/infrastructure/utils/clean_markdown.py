import re


def clean_markdown(
    markdown: str,
) -> str:
    # 1. Удаляем блоки стилей, скриптов и svg, которые создают "шум"
    markdown = re.sub(
        r"<style.*?>.*?</style>", "", markdown, flags=re.DOTALL | re.IGNORECASE
    )
    markdown = re.sub(
        r"<script.*?>.*?</script>", "", markdown, flags=re.DOTALL | re.IGNORECASE
    )
    markdown = re.sub(
        r"<svg.*?>.*?</svg>", "", markdown, flags=re.DOTALL | re.IGNORECASE
    )

    # 2. Оставляем только важные для карточек теги, если нужно (опционально)
    # 3. Обрезаем лишние пробелы и пустые строки
    markdown = re.sub(r"\n\s*\n", "\n", markdown)

    return markdown
