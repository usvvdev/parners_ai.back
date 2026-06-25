# packages

from asyncio import run

from pathlib import Path

from loguru import logger

import torch

# application depencies

from libs.infrastructure.factories.common import ApplicationConfigFactory

from .src.infrastructure.factories.services import ParserAgentServiceFactory


torch.backends.nnpack.set_flags(False)


SERVICE_DIR = Path(__file__).parent


async def run_app() -> None:
    config = ApplicationConfigFactory.create(
        service_dir=SERVICE_DIR,
    )

    agent = ParserAgentServiceFactory.create(
        config=config,
    )

    try:
        results = await agent.execute()

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
        await agent._api_clients.close()


def main() -> None:
    run(run_app())


if __name__ == "__main__":
    main()
