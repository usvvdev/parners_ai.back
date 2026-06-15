from asyncio import run

from pathlib import Path

from loguru import logger

from .src.infrastructure.factories import (
    APIClientsFactory,
    AgentServicesFactory,
)

from libs.infrastructure.factories.common import ApplicationConfigFactory


SERVICE_DIR = Path(__file__).parent


async def run_app() -> None:
    config = ApplicationConfigFactory.create(
        service_dir=SERVICE_DIR,
    )

    print(config)

    clients = APIClientsFactory.create(
        config=config,
    )

    services = AgentServicesFactory.create(
        config=config,
        clients=clients,
    )

    try:
        results = await services.parser.execute()

        for result in results:
            for offer in result.target_offers_found:
                if not offer.is_found:
                    continue

                logger.info(
                    "Offer '{}' found at position {} on {}",
                    offer.title,
                    offer.position,
                    result.link,
                )
    finally:
        await clients.close()


def main() -> None:
    run(run_app())


if __name__ == "__main__":
    main()
