from asyncio import run

from src.domain.types.partner_result import PartnerResult

from src.infrastructure.factories import BrowserAgentFactory


# 1. Rename your async function to something descriptive
async def run_browser_agent() -> PartnerResult:
    browser_agent = BrowserAgentFactory.create()

    result = await browser_agent.parse(
        link="https://vauzaem.ru/offers",
        target_offers=[
            "Zaymigo",
        ],
    )

    for offer in result.target_offers_found:
        print(f"🎯 Оффер '{offer.title}' найден на позиции №{offer.position}")

    return result


# 2. Create a standard synchronous 'main' function for the CLI entry point
def main():
    """Synchronous entry point for the console script."""
    run(run_browser_agent())


# 3. Keep this so you can still run the file directly if needed
if __name__ == "__main__":
    main()
