# packages

from asyncio import run

from pathlib import Path

from loguru import logger

from aiogram import Bot, Dispatcher

from aiogram.client.session.aiohttp import AiohttpSession

# application dependencies

from .src.interface.routing import BotApplicationRouter

from .src.interface.api.routes import (
    start_router,
    main_router,
    partner_router,
    link_router,
    offer_router,
)

from .src.infrastructure.factories import (
    APIClientsFactory,
    BotServicesFactory,
)

from libs.infrastructure.factories.common import ApplicationConfigFactory


SERVICE_DIR = Path(__file__).parent


async def create_app() -> None:
    config = ApplicationConfigFactory.create(
        service_dir=SERVICE_DIR,
    )

    clients = APIClientsFactory.create(
        config=config,
    )

    services = BotServicesFactory.create(
        clients=clients,
    )

    bot = Bot(
        token=config.telegram_options.bot_token,
        session=AiohttpSession(
            config.proxy_url,
        ),
    )

    dp = Dispatcher()

    dp["partner_service"] = services.partner
    dp["link_service"] = services.link
    dp["offer_service"] = services.offer

    BotApplicationRouter(
        dispatcher=dp,
    ).register_routes(
        routes=[
            start_router,
            main_router,
            partner_router,
            link_router,
            offer_router,
        ],
    )

    try:
        logger.info("Bot starting...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await clients.close()
        await bot.session.close()
        logger.info("Bot stopped")


def main():
    run(
        create_app(),
    )


if __name__ == "__main__":
    main()
