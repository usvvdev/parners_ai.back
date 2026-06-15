# packages

from loguru import logger

# application dependencies

from ...domain.types._types import (
    FetchLinks,
    FetchOffer,
    InsertOfferPosition,
    InsertPartner,
    InsertUTMSource,
    PartnerResult,
    UpdatePartner,
)
from ...domain.utils.parse_url import extract_query_param
from .browser_agent import BrowserAgentService

from ...infrastructure.clients.api import (
    LinkAPIClient,
    OfferAPIClient,
    PartnerAPIClient,
    UTMSourceAPIClient,
    OfferPositionAPIClient,
)


class ParserAgentService:
    def __init__(
        self,
        browser_agent: BrowserAgentService,
        link_client: LinkAPIClient,
        offer_client: OfferAPIClient,
        partner_client: PartnerAPIClient,
        utm_source_client: UTMSourceAPIClient,
        offer_position_client: OfferPositionAPIClient,
    ) -> None:
        self._browser_agent = browser_agent
        self._link_client = link_client
        self._offer_client = offer_client
        self._partner_client = partner_client
        self._utm_source_client = utm_source_client
        self._offer_position_client = offer_position_client

    @staticmethod
    def _resolve_target_titles(
        link: FetchLinks,
        all_offers: list[FetchOffer],
    ) -> list[str]:
        if link.offers:
            symbols = set(link.offers)
            titles = [offer.title for offer in all_offers if offer.symbol in symbols]
            if titles:
                return titles

        return [offer.title for offer in all_offers]

    async def _resolve_utm_source_id(
        self,
        title: str,
    ) -> int:
        normalized = title.strip().lower()

        for source in await self._utm_source_client.fetch_all():
            if source.title.strip().lower() == normalized:
                return source.id

        created = await self._utm_source_client.create(
            InsertUTMSource(title=title.strip()),
        )
        return created.id

    async def _bind_partner(
        self,
        *,
        wmid: str,
        utm_source: str,
        link_id: int,
    ) -> None:
        utm_source_id = await self._resolve_utm_source_id(utm_source)

        existing = next(
            (
                partner
                for partner in await self._partner_client.fetch_all()
                if partner.wmid == wmid
            ),
            None,
        )

        if existing is None:
            await self._partner_client.create(
                InsertPartner(
                    wmid=wmid,
                    utm_source_id=utm_source_id,
                    link_ids=[link_id],
                ),
            )
            return

        partner = await self._partner_client.fetch_by_id(existing.id)
        link_ids = {item.id for item in partner.links.items}
        link_ids.add(link_id)

        await self._partner_client.update(
            existing.id,
            UpdatePartner(
                link_ids=list(link_ids),
            ),
        )

    async def _persist_scan_result(
        self,
        *,
        link: FetchLinks,
        result: PartnerResult,
    ) -> None:
        for offer in result.target_offers_found:
            if not offer.is_found:
                continue

            wmid = extract_query_param(offer.url, "wmid")
            utm_source = extract_query_param(offer.url, "utm_source")

            if not wmid or not utm_source:
                logger.warning(
                    "Skip offer without wmid/utm_source: link={} offer={} url={}",
                    link.link,
                    offer.title,
                    offer.url,
                )
                continue

            await self._bind_partner(
                wmid=wmid,
                utm_source=utm_source,
                link_id=link.id,
            )

            await self._offer_position_client.create(
                InsertOfferPosition(
                    wmid=wmid,
                    utm_source=utm_source,
                    offer=offer.title,
                    vitrina=link.link,
                    position=offer.position,
                ),
            )

    async def execute(self) -> list[PartnerResult]:
        links = [link for link in await self._link_client.fetch_all() if link.is_active]
        all_offers = await self._offer_client.fetch_all()

        results: list[PartnerResult] = []

        for link in links:
            target_offers = self._resolve_target_titles(
                link,
                all_offers,
            )

            if not target_offers:
                logger.warning(
                    "Skip link without target offers: {}",
                    link.link,
                )
                continue

            logger.info(
                "Scanning {} with targets: {}",
                link.link,
                ", ".join(target_offers),
            )

            result = await self._browser_agent.parse(
                link=link.link,
                target_offers=target_offers,
            )

            await self._persist_scan_result(
                link=link,
                result=result,
            )

            results.append(result)

        return results
