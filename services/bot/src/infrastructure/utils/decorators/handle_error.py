# packages

from typing import Callable

from functools import wraps

from httpx import HTTPStatusError


def handle_http_error(message: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(callback, *args, **kwargs):
            try:
                return await func(callback, *args, **kwargs)
            except HTTPStatusError as err:
                raise err

        return wrapper

    return decorator
