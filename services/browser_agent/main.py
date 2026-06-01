from asyncio import run

from pathlib import Path

from .src.infrastructure.factories import PartnerParserServiceFactory

from libs.infrastructure.factories.common import ApplicationConfigFactory


# 1. Rename your async function to something descriptive
async def run_app() -> None:
    config = ApplicationConfigFactory.create(
        service_dir=Path(__file__).parent,
    )

    service = PartnerParserServiceFactory.create(
        config=config,
    )

    results = await service.execute()

    for result in results:
        for offer in result.target_offers_found:
            print(
                f"🎯 Оффер '{offer.title}' найден на позиции №{offer.position}. У партнера: {result}"
            )


# # 2. Create a standard synchronous 'main' function for the CLI entry point
def main():
    """Synchronous entry point for the console script."""
    run(run_app())


# # 3. Keep this so you can still run the file directly if needed
if __name__ == "__main__":
    main()
