from typing import Optional

import urllib.parse as urlparse

from urllib.parse import parse_qs


def parse_url(
    url: str,
    get_params: list[str, ...],
) -> list[dict[str, Optional[str]]]:
    parsed_url = urlparse.urlparse(url)

    params = parse_qs(
        parsed_url.query,
    )
    return [{param: params.get(param)} for param in get_params]
