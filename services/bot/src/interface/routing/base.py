# packages

from aiogram import Dispatcher

from aiogram import Router


class BotApplicationRouter:
    def __init__(
        self,
        dispatcher: Dispatcher,
    ) -> None:
        self._dispatcher = dispatcher

    def register_routes(
        self,
        *,
        routes: list[Router],
    ) -> None:
        for route in routes:
            self._dispatcher.include_router(route)
