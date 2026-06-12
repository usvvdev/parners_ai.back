from html import escape


def safe(value: str) -> str:
    return escape(value, quote=True)


def short_url(value: str, limit: int = 35) -> str:
    url = value.replace("https://", "").replace("http://", "")

    return f"{url[:limit]}..." if len(url) > limit else url
