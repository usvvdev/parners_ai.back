from typing import Callable

from functools import wraps

from fastapi_pagination.utils import disable_installed_extensions_check


def disable_extension_check(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        disable_installed_extensions_check()

        return await func(*args, **kwargs)

    return wrapper
