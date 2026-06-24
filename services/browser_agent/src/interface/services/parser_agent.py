# packages

from loguru import logger

from datetime import datetime

# application dependencies

from .browser_agent import BrowserAgentService

from ...domain.types._types import PartnerResult

from libs.domain.types._types.shared import APIClients

from libs.infrastructure.clients.http.schemas import (
    FetchLinks,
    FetchOffer,
    InsertOfferPosition,
    InsertPartner,
    InsertUTMSource,
    UpdatePartner,
)


class ParserAgentService:
    def __init__(
        self,
        browser_agent: BrowserAgentService,
        api_clients: APIClients,
    ) -> None:
        self._browser_agent = browser_agent
        self._api_clients = api_clients
        self._default_offers: list[FetchOffer] | None = None

    async def _get_default_offers(self) -> list[FetchOffer]:
        if self._default_offers is None:
            self._default_offers = await self._api_clients.offer.fetch_all()
            logger.info(
                "Cached {} default offers",
                len(self._default_offers),
            )

        return self._default_offers

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

        for source in await self._api_clients.utm_source.fetch_all():
            if source.title.strip().lower() == normalized:
                return source.id

        created = await self._api_clients.utm_source.create(
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
                for partner in await self._api_clients.partner.fetch_all()
                if partner.wmid == wmid
            ),
            None,
        )

        if existing is None:
            await self._api_clients.partner.create(
                InsertPartner(
                    wmid=wmid,
                    utm_source_id=utm_source_id,
                    link_ids=[link_id],
                ),
            )
            return

        partner = await self._api_clients.partner.fetch_by_id(existing.id)
        link_ids = {item.id for item in partner.links.items}
        link_ids.add(link_id)

        await self._api_clients.partner.update(
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

            wmid = offer.wmid or None
            utm_source = offer.utm_source or None

            if not wmid or not utm_source:
                logger.warning(
                    "Skip offer without wmid/utm_source: link={} offer={} url={} final_url={}",
                    link.link,
                    offer.title,
                    offer.url,
                    offer.final_url,
                )
                continue

            await self._bind_partner(
                wmid=wmid,
                utm_source=utm_source,
                link_id=link.id,
            )

            await self._api_clients.offer_position.create(
                InsertOfferPosition(
                    wmid=wmid,
                    utm_source=utm_source,
                    offer=offer.title,
                    vitrina=link.link,
                    position=offer.position,
                    created_at=datetime.now(),
                ),
            )

    async def execute(self) -> list[PartnerResult]:
        links = await self._api_clients.link.fetch_all()
        all_offers = await self._get_default_offers()

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
