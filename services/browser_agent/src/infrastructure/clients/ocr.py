# packages

import asyncio

import base64

import re

from functools import lru_cache

from html import unescape

from urllib.parse import urljoin

import httpx

from bs4 import BeautifulSoup, Tag

from loguru import logger

from playwright.async_api import async_playwright

from rapidfuzz import fuzz
from rapidfuzz import process as fuzz_process

# application dependencies

from ...domain.types._types import PartnerResult
from ...domain.types._types.scanned_offer import ScannedOffer
from ...domain.protocols.agent import ICrawlerProtocol, IOCRProtocol
from ...infrastructure.utils.parse_url import extract_query_param


_RE_OFFER_CARD = re.compile(
    r'window\.open\([\'"](?P<cta>[^\'"]+)[\'"]\).*?'
    r'<img[^>]+src=[\'"](?P<logo>[^\'"]+)[\'"].*?'
    r"<strong>(?P<text>.*?)</strong>",
    re.DOTALL,
)

# data:image/png;base64,....
_RE_DATA_URI = re.compile(r"^data:image/[a-zA-Z+]+;base64,(.+)$")

_HTTP_TIMEOUT_S = 10.0
_SVG_RENDER_SIZE = 512

# Порог fuzzy-матчинга по имени (token_set_ratio)
_NAME_MATCH_THRESHOLD = 80
# Порог fuzzy-матчинга по OCR-тексту (WRatio)
_OCR_MATCH_THRESHOLD = 85


# ---------------------------------------------------------------------------
# DOM-утилиты (портированы из test.py)
# ---------------------------------------------------------------------------


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _abs_url(base: str, href: str) -> str:
    if not href or href.startswith(("http://", "https://")):
        return href.strip()
    return urljoin(base, href.strip())


def _extract_url(tag: Tag) -> str:
    """Извлекает URL из атрибутов тега или его onclick."""
    for attr in ("href", "data-href"):
        val = tag.get(attr, "")
        if val and val not in ("#", "javascript:void(0)", "javascript:;"):
            return val

    onclick = unescape(tag.get("onclick") or tag.get("data-onclick") or "")
    if onclick:
        if m := re.search(r"window\.open\(['\"]([^'\"]+)['\"]", onclick):
            return m.group(1)
        if m := re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", onclick):
            return m.group(1)
        if m := re.search(r"(https?://[^'\"\)\s]+)", onclick):
            return m.group(1)
    return ""


def _get_primary_link(tag: Tag) -> str:
    """
    Универсальный поиск ссылки блока.
    Приоритет: 1) Ссылки с параметрами (трекеры) 2) Обычные ссылки 3) Onclick
    """
    if url := _extract_url(tag):
        return url

    links_with_params, links_without_params = [], []

    for a in tag.find_all("a", recursive=True):
        if url := _extract_url(a):
            (links_with_params if "?" in url else links_without_params).append(url)

    if links_with_params:
        return links_with_params[0]
    if links_without_params:
        return links_without_params[0]

    for el in tag.find_all(True, recursive=True):
        if url := _extract_url(el):
            return url

    return ""


def _get_first_img(tag: Tag) -> Tag | None:
    """Возвращает первый тег <img> с заполненным src."""
    for img in tag.find_all("img"):
        if img.get("src") or img.get("data-src"):
            return img
    return None


def _get_offer_name(tag: Tag, logo: Tag | None) -> str:
    """Извлекает название оффера из атрибутов, без поиска по тегам текста."""
    # 1. Атрибут name / data-name
    if name := _clean(tag.get("name") or tag.get("data-name") or ""):
        return name

    # 2. Alt логотипа
    if logo and (alt := _clean(logo.get("alt") or "")):
        return alt

    # 3. GTM dataLayer (ищет 'name': 'значение' в onclick)
    for el in [tag] + tag.find_all(True):
        onclick = unescape(el.get("onclick") or "")
        if m := re.search(r"['\"]name['\"]\s*:\s*['\"]([^'\"]{3,})['\"]", onclick):
            raw = m.group(1)
            if raw.lower() not in ("click_offer", "gtm-ee-event", "product clicks"):
                if clean_name := _clean(
                    re.sub(
                        r"\s*[-–]\s*(Выдача|RevShare|CPA|CPL).*$", "", raw, flags=re.I
                    )
                ):
                    return clean_name

    # 4. Имя файла логотипа (если не хэш)
    if logo and (src := logo.get("src") or logo.get("data-src") or ""):
        fname = re.sub(r"\.[a-zA-Z]+$", "", src.rstrip("/").split("/")[-1])
        if not re.match(r"^[0-9a-f]{8,}[\.\d]*$", fname, re.I):
            fname = re.sub(
                r"[-_]",
                " ",
                re.sub(r"\b(logo|img|image|icon)\b", "", fname, flags=re.I),
            )
            if len(clean_fname := _clean(fname)) > 2:
                return clean_fname

    return ""


def _detect_cards_from_html(
    html: str,
    base_url: str = "",
) -> list[tuple[str, str, str]]:
    """
    Парсит HTML страницы-витрины и возвращает список
    (offer_url, logo_src, offer_name) для каждой найденной карточки.

    Карточка — любой блок с текстом, картинкой и кликабельной ссылкой.
    Дублирующиеся родительские блоки отсекаются (оставляются листья DOM).
    """
    soup = BeautifulSoup(html, "html.parser")
    candidates: list[tuple[Tag, str]] = []

    for tag in soup.find_all(["div", "article", "section", "li", "a"]):
        text = _clean(tag.get_text(" "))
        if not (10 < len(text) < 2000):
            continue
        if not tag.find("img"):
            continue

        offer_url = _get_primary_link(tag)
        if not offer_url:
            continue

        candidates.append((tag, offer_url))

    # Оставляем только «листья» DOM-дерева
    leafs = [
        (tag, url)
        for tag, url in candidates
        if not any(tag in other.parents for other, _ in candidates if other is not tag)
    ]

    # Дедупликация по (ссылка, лого)
    seen: set[tuple[str, str]] = set()
    result: list[tuple[str, str, str]] = []

    for tag, raw_url in leafs:
        logo_img = _get_first_img(tag)
        logo_src = (
            _abs_url(base_url, logo_img.get("src") or logo_img.get("data-src") or "")
            if logo_img
            else ""
        )
        offer_url = _abs_url(base_url, raw_url)
        key = (offer_url, logo_src)
        if key not in seen:
            seen.add(key)
            offer_name = _get_offer_name(tag, logo_img)
            result.append((offer_url, logo_src, offer_name))

    return result


def _match_by_name(
    name: str,
    known: list[str],
    threshold: int = _NAME_MATCH_THRESHOLD,
) -> tuple[str | None, float]:
    """Fuzzy-матчинг по имени (token_set_ratio). Возвращает (offer, score) или (None, 0)."""
    if not name or not known:
        return None, 0.0

    # Точное совпадение
    if exact := next((k for k in known if k.lower() == name.lower()), None):
        return exact, 100.0

    if res := fuzz_process.extractOne(
        name, known, scorer=fuzz.token_set_ratio, score_cutoff=threshold
    ):
        return res[0], float(res[1])

    return None, 0.0


class _Card:
    """Нормализованное представление карточки оффера."""

    def __init__(
        self,
        position: int,
        logo_src: str,
        url: str,
        offer_name: str = "",
    ) -> None:
        self.position = position
        self.logo_src = logo_src
        self.url = url
        self.offer_name = offer_name


class OCRAgent(IOCRProtocol):
    """
    Анализирует страницу-витрину и сопоставляет карточки офферов с целевыми.

    Извлечение карточек:
      Парсит HTML страницы через BeautifulSoup: карточка — любой блок
      с текстом (10–2000 символов), картинкой и кликабельной ссылкой.
      Родительские дубликаты отсекаются, итог дедуплицируется по (url, logo).

    Матчинг (двухступенчатый):
      1. Первичный — по имени оффера (из alt/атрибутов/onclick/filename),
         fuzzy token_set_ratio >= 80.
      2. Fallback — OCR логотипа (EasyOCR, ru+en), WRatio >= 85.

    После матчинга:
      - Редиректы запускаются параллельно через asyncio.gather.
      - Из финального URL извлекаются wmid и utm_source.
      - Результат пишется в ClickHouse через ParserAgentService.
    """

    def __init__(self, crawler: ICrawlerProtocol) -> None:
        self._crawler = crawler
        self._http_client = httpx.AsyncClient(timeout=_HTTP_TIMEOUT_S)
        self._playwright = None
        self._browser = None
        self._browser_lock = asyncio.Lock()

    async def aclose(self) -> None:
        """Закрывает HTTP-клиент и браузер для SVG-рендеринга (если был запущен)."""
        await self._http_client.aclose()
        if self._browser is not None:
            await self._browser.close()
        if self._playwright is not None:
            await self._playwright.stop()

    async def _get_browser(self):
        # Ленивая инициализация — браузер запускается один раз и переиспользуется
        # для всех SVG-логотипов за время жизни OCRAgent.
        if self._browser is None:
            async with self._browser_lock:
                if self._browser is None:
                    self._playwright = await async_playwright().start()
                    self._browser = await self._playwright.chromium.launch(
                        headless=True,
                    )
        return self._browser

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def analyze(
        self,
        *,
        showcase_url: str,
        target_offers: list[str],
        html: str = "",
        markdown: str = "",
        screenshot: str = "",
    ) -> PartnerResult:
        # 1. Извлекаем карточки из HTML витрины
        raw_cards = _detect_cards_from_html(html, base_url=showcase_url) if html else []

        # Fallback на markdown-парсинг, если HTML пустой
        if not raw_cards and markdown:
            raw_cards = self._parse_markdown_cards(markdown, base_url=showcase_url)

        cards = [
            _Card(pos, logo_src, url, offer_name)
            for pos, (url, logo_src, offer_name) in enumerate(raw_cards, start=1)
        ]
        logger.debug(
            "Extracted {} cards from {} (showcase={})",
            len(cards),
            "html" if html else "markdown",
            showcase_url,
        )

        # 2. Матчинг: имя → OCR fallback (параллельно по карточкам)
        async def match(card: _Card) -> tuple[_Card, str, float] | None:
            # Первичный матчинг по имени из DOM
            matched_title, score = _match_by_name(card.offer_name, target_offers)
            if matched_title:
                logger.debug(
                    "Card {}: name-match {!r} (name={!r}, score={:.0f})",
                    card.position,
                    matched_title,
                    card.offer_name,
                    score,
                )
                return card, matched_title, score

            # Fallback: OCR логотипа
            if card.logo_src:
                ocr_text = await self._ocr_logo(card.logo_src)
                if ocr_text:
                    ocr_result = self._match_ocr_text(ocr_text, target_offers)
                    if ocr_result:
                        ocr_title, ocr_score = ocr_result
                        logger.debug(
                            "Card {}: ocr-match {!r} (ocr={!r}, score={:.0f})",
                            card.position,
                            ocr_title,
                            ocr_text,
                            ocr_score,
                        )
                        return card, ocr_title, ocr_score
                    else:
                        logger.debug(
                            "Card {}: no match (name={!r}, ocr={!r})",
                            card.position,
                            card.offer_name,
                            ocr_text,
                        )
                else:
                    logger.debug(
                        "Card {}: OCR returned empty text (name={!r})",
                        card.position,
                        card.offer_name,
                    )
            else:
                logger.debug(
                    "Card {}: no logo src, skipping OCR (name={!r})",
                    card.position,
                    card.offer_name,
                )

            return None

        match_results = await asyncio.gather(*[match(card) for card in cards])

        matched: list[tuple[_Card, str, float]] = []
        seen: set[str] = set()
        for result in match_results:
            if result is None:
                continue
            card, title, score = result
            if title in seen:
                continue
            seen.add(title)
            matched.append((card, title, score))

        # 3. Параллельный резолв редиректов для совпавших карточек
        async def resolve(card: _Card, title: str, score: float) -> ScannedOffer:
            final_url, wmid, utm_source = await self._resolve_redirect(card.url)
            logger.info(
                "Card {}: {!r} wmid={!r} utm={!r} url={!r}",
                card.position,
                title,
                wmid,
                utm_source,
                card.url,
            )
            return ScannedOffer(
                title=title,
                position=card.position,
                is_found=True,
                url=card.url,
                final_url=final_url,
                wmid=wmid or "",
                utm_source=utm_source or "",
                offer_name=card.offer_name,
                match_score=round(score, 1),
            )

        found: list[ScannedOffer] = await asyncio.gather(
            *[resolve(card, title, score) for card, title, score in matched]
        )

        found.sort(key=lambda o: o.position)

        return PartnerResult(
            link=showcase_url,
            total_cards=len(cards),
            target_offers_found=found,
        )

    # ------------------------------------------------------------------
    # Card extraction
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_markdown_cards(
        markdown: str,
        base_url: str = "",
    ) -> list[tuple[str, str, str]]:
        """
        Fallback: парсит карточки-офферы из markdown-представления страницы.
        Используется только если HTML недоступен.

        Возвращает список (offer_url, logo_src, offer_name).
        """
        if not markdown:
            return []

        result: list[tuple[str, str, str]] = []

        for match in _RE_OFFER_CARD.finditer(markdown):
            logo_src = match.group("logo").strip()
            cta_url = match.group("cta").strip()
            text = re.sub(r"\s+", " ", match.group("text")).strip()

            if not logo_src or not text:
                continue

            offer_url = _abs_url(base_url, cta_url)
            logo_abs = _abs_url(base_url, logo_src)
            result.append((offer_url, logo_abs, ""))

        return result

    # ------------------------------------------------------------------
    # OCR
    # ------------------------------------------------------------------

    @staticmethod
    @lru_cache(maxsize=1)
    def _get_reader():
        # Ленивая инициализация — модель грузится один раз на процесс.
        import easyocr

        return easyocr.Reader(["ru", "en"], gpu=False)

    async def _fetch_logo_bytes(self, logo_src: str) -> tuple[bytes, str] | None:
        data_uri_match = _RE_DATA_URI.match(logo_src)
        if data_uri_match:
            mime = re.match(r"^data:(image/[a-zA-Z+]+);base64,", logo_src)
            content_type = mime.group(1) if mime else ""
            try:
                return base64.b64decode(data_uri_match.group(1)), content_type
            except (ValueError, base64.binascii.Error) as err:
                logger.warning("Failed to decode data URI logo: {}", err)
                return None

        try:
            response = await self._http_client.get(logo_src)
            response.raise_for_status()
        except httpx.HTTPError as err:
            logger.warning("Failed to fetch logo {!r}: {}", logo_src, err)
            return None

        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            logger.warning(
                "Logo {!r} returned non-image content-type {!r}, skipping",
                logo_src,
                content_type,
            )
            return None

        if not response.content:
            logger.warning("Logo {!r} returned empty body", logo_src)
            return None

        return response.content, content_type

    @staticmethod
    def _is_svg(image_bytes: bytes, content_type: str) -> bool:
        if "svg" in content_type.lower():
            return True
        head = image_bytes[:256].lstrip()
        return head.startswith(b"<?xml") or head.startswith(b"<svg")

    async def _rasterize_svg(self, svg_bytes: bytes, logo_src: str) -> bytes | None:
        """
        Растеризует SVG в PNG через headless Chromium (Playwright) — без
        системных зависимостей типа libcairo. SVG встраивается через <img>
        в собственный минимальный HTML-документ (а не загружается напрямую
        как top-level data URI — в этом случае Chromium открывает его как
        спец. image-viewer документ без <body>), затем делается screenshot
        контейнера с картинкой.
        """
        try:
            browser = await self._get_browser()
            page = await browser.new_page(
                viewport={"width": _SVG_RENDER_SIZE, "height": _SVG_RENDER_SIZE},
            )
            try:
                svg_data_uri = (
                    "data:image/svg+xml;base64," + base64.b64encode(svg_bytes).decode()
                )
                html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  html, body {{ margin: 0; padding: 0; background: white; }}
  #logo {{ display: block; max-width: 100%; height: auto; }}
</style>
</head>
<body>
  <img id="logo" src="{svg_data_uri}">
</body>
</html>"""
                await page.set_content(html, timeout=_HTTP_TIMEOUT_S * 1000)
                logo_el = page.locator("#logo")
                await logo_el.wait_for(state="visible", timeout=_HTTP_TIMEOUT_S * 1000)
                return await logo_el.screenshot(type="png")
            finally:
                await page.close()
        except Exception as err:
            logger.warning("Failed to rasterize SVG logo {!r}: {}", logo_src, err)
            return None

    async def _decode_image_rgb(
        self, image_bytes: bytes, content_type: str, logo_src: str
    ):
        """
        Декодирует байты изображения в numpy-массив RGB, готовый для EasyOCR.
        SVG растеризуется через headless Chromium в PNG, остальные растровые
        форматы читаются через Pillow. Возвращает None, если изображение
        повреждено/не распознано — без падения в недрах OpenCV.
        """
        import numpy as np
        from PIL import Image, UnidentifiedImageError
        from io import BytesIO

        if self._is_svg(image_bytes, content_type):
            image_bytes = await self._rasterize_svg(image_bytes, logo_src)
            if image_bytes is None:
                return None

        loop = asyncio.get_running_loop()

        def decode() -> object | None:
            try:
                with Image.open(BytesIO(image_bytes)) as img:
                    img.load()
                    return np.array(img.convert("RGB"))
            except (UnidentifiedImageError, OSError, ValueError) as err:
                logger.warning("Failed to decode logo image {!r}: {}", logo_src, err)
                return None

        return await loop.run_in_executor(None, decode)

    async def _ocr_logo(self, logo_src: str) -> str:
        if not logo_src:
            return ""

        fetched = await self._fetch_logo_bytes(logo_src)
        if not fetched:
            return ""
        image_bytes, content_type = fetched

        image_rgb = await self._decode_image_rgb(image_bytes, content_type, logo_src)
        if image_rgb is None:
            return ""

        loop = asyncio.get_running_loop()
        try:
            lines: list[str] = await loop.run_in_executor(
                None,
                lambda: self._get_reader().readtext(image_rgb, detail=0),
            )
        except Exception as err:
            logger.warning("OCR failed for logo {!r}: {}", logo_src, err)
            return ""

        return " ".join(line.strip() for line in lines if line.strip())

    # ------------------------------------------------------------------
    # Matching
    # ------------------------------------------------------------------

    @staticmethod
    def _match_ocr_text(
        ocr_text: str,
        target_offers: list[str],
    ) -> tuple[str, float] | None:
        """
        Сравнивает OCR-текст с каждым target_offer через WRatio.
        Возвращает (title, score) с наибольшим score >= _OCR_MATCH_THRESHOLD, иначе None.
        """
        best_title: str | None = None
        best_score: float = 0.0

        for offer in target_offers:
            score = fuzz.WRatio(ocr_text.lower(), offer.lower())
            if score >= _OCR_MATCH_THRESHOLD and score > best_score:
                best_score = score
                best_title = offer

        if best_title is None:
            return None

        return best_title, best_score

    # ------------------------------------------------------------------
    # Redirect resolution
    # ------------------------------------------------------------------

    async def _resolve_redirect(
        self,
        url: str,
    ) -> tuple[str, str | None, str | None]:
        if not url:
            return url, None, None

        try:
            final_url = await self._crawler.navigate_and_capture_url(link=url)
        except RuntimeError as err:
            logger.warning("Redirect failed for {!r}: {}", url, err)
            return url, None, None

        wmid = extract_query_param(final_url, "wmid")
        utm_source = extract_query_param(final_url, "utm_source")

        return final_url, wmid, utm_source
