# packages

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    CrawlResult,
)

# application dependencies

from ....domain.protocols import ICrawlerProtocol


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
