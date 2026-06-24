from urllib.parse import parse_qs, urlparse


def extract_query_param(
    url: str,
    param: str,
) -> str | None:
    if not url:
        return None

    values = parse_qs(
        urlparse(url).query,
    ).get(param)

    if not values:
        return None

    return values[0] or None
