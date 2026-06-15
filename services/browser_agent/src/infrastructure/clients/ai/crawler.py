# packages

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    CrawlResult,
)
from playwright.async_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)

# application dependencies

from ....domain.protocols import ICrawlerProtocol

_NAVIGATION_TIMEOUT_MS = 30_000
_POPUP_WAIT_MS = 15_000
_REDIRECT_SETTLE_MS = 2_000
_POPUP_POLL_MS = 200


class Crawler(
    ICrawlerProtocol,
):
    def __init__(
        self,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
    ) -> None:
        self._viewport_width = viewport_width
        self._viewport_height = viewport_height

        self._browser_config = BrowserConfig(
            headless=True,
            viewport_width=self._viewport_width,
            viewport_height=self._viewport_height,
        )

        self._run_config = CrawlerRunConfig(
            screenshot=True,
            magic=True,
            delay_before_return_html=3.0,
            cache_mode=CacheMode.BYPASS,
        )

    async def crawl(
        self,
        *,
        link: str,
    ) -> CrawlResult:
        async with AsyncWebCrawler(
            config=self._browser_config,
        ) as crawler:
            try:
                result: CrawlResult = await crawler.arun(
                    url=link,
                    config=self._run_config,
                )
            except Exception as err:
                raise RuntimeError(
                    f"Error during crawling: {str(err)}",
                )

        if not result.success or not result.screenshot:
            raise RuntimeError(
                result.error_message if not result.success else "Screenshot not found",
            )

        return result

    @staticmethod
    async def _wait_for_popup_page(
        *,
        context,
        initial_page: Page,
        timeout_ms: int = _POPUP_WAIT_MS,
    ) -> Page:
        elapsed = 0

        while elapsed < timeout_ms:
            pages = context.pages
            if len(pages) > 1:
                return pages[-1]

            await initial_page.wait_for_timeout(_POPUP_POLL_MS)
            elapsed += _POPUP_POLL_MS

        return initial_page

    async def navigate_and_capture_url(
        self,
        *,
        link: str,
    ) -> str:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=True,
            )
            context = await browser.new_context(
                viewport={
                    "width": self._viewport_width,
                    "height": self._viewport_height,
                },
            )

            try:
                page = await context.new_page()
                target_page = page

                try:
                    async with context.expect_page(
                        timeout=_POPUP_WAIT_MS,
                    ) as new_page_info:
                        await page.goto(
                            link,
                            wait_until="domcontentloaded",
                            timeout=_NAVIGATION_TIMEOUT_MS,
                        )
                    target_page = await new_page_info.value
                except PlaywrightTimeoutError:
                    await page.wait_for_load_state(
                        "domcontentloaded",
                        timeout=_NAVIGATION_TIMEOUT_MS,
                    )
                    target_page = await self._wait_for_popup_page(
                        context=context,
                        initial_page=page,
                    )

                if target_page is page and len(context.pages) > 1:
                    target_page = context.pages[-1]

                await target_page.wait_for_load_state(
                    "domcontentloaded",
                    timeout=_NAVIGATION_TIMEOUT_MS,
                )
                await target_page.wait_for_timeout(_REDIRECT_SETTLE_MS)

                return target_page.url or link
            except Exception as err:
                raise RuntimeError(
                    f"Error during offer redirect capture: {str(err)}",
                ) from err
            finally:
                await context.close()
                await browser.close()
