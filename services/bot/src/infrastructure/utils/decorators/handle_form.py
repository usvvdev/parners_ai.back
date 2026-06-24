# packages

from typing import Callable

from functools import wraps

from httpx import HTTPStatusError

# application depencies

from ..functions.filter_state import clear_state_keep_filters

from ..functions.chat import (
    delete_user_message,
    edit_menu_message,
)


def handle_form_submit(error_message: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(message, *args, **kwargs):
            state = kwargs.get("state")

            await delete_user_message(message)

            try:
                text, markup = await func(message, *args, **kwargs)
            except HTTPStatusError:
                await edit_menu_message(
                    message.bot,
                    state,
                    error_message,
                )
                await clear_state_keep_filters(state)
                return

            await edit_menu_message(
                message.bot,
                state,
                text,
                markup,
            )
            await clear_state_keep_filters(state)

        return wrapper

    return decorator
