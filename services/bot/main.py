# packages

import asyncio

from pathlib import Path

from loguru import logger

from aiogram import Bot, Dispatcher

from aiogram.client.session.aiohttp import AiohttpSession

# application dependencies

from .src.config import BotSettings

from .src.interface.handlers import (
    start_router,
    partner_router,
    link_router,
    offer_router,
    main_router,
)

from .src.infrastructure.factories import APIClientsFactory


SERVICE_DIR = Path(__file__).parent


async def run_app() -> None:
    settings = BotSettings(
        _env_file=SERVICE_DIR / ".env",
    )

    clients = APIClientsFactory.create(
        base_url=settings.api_base_url,
    )

    session = AiohttpSession(
        settings.proxy_url,
    )

    bot = Bot(
        token=settings.bot_token,
        session=session,
    )

    dp = Dispatcher()

    dp["partner_client"] = clients.partner
    dp["link_client"] = clients.link
    dp["offer_client"] = clients.offer

    dp.include_router(start_router)
    dp.include_router(main_router)
    dp.include_router(partner_router)
    dp.include_router(link_router)
    dp.include_router(offer_router)

    try:
        logger.info("Bot starting...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await clients.close()
        await bot.session.close()
        logger.info("Bot stopped")


def main():
    asyncio.run(run_app())


if __name__ == "__main__":
    main()
