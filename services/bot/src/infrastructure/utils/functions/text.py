from html import escape


def safe(value: str) -> str:
    return escape(value, quote=True)


def short_url(value: str, limit: int = 35) -> str:
    url = value.replace("https://", "").replace("http://", "").rstrip("/")

    return f"{url[:limit]}..." if len(url) > limit else url


def format_offer_symbols(symbols: list[str]) -> str:
    if not symbols:
        return ""

    return "·".join(symbols)


def format_offer_button_label(
    *,
    symbol: str,
    title: str,
) -> str:
    if symbol:
        return f"{symbol} · {title}"

    return title


def format_link_list_label(
    link: str,
    symbols: list[str],
    *,
    url_limit: int = 28,
) -> str:
    badges = format_offer_symbols(symbols)
    url = short_url(link, limit=url_limit)

    badge_part = f" [{badges}]" if badges else ""

    return f" {badge_part} {url}"
