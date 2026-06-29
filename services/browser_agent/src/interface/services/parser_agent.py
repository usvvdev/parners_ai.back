# packages

from loguru import logger

from datetime import datetime

# application dependencies

from .browser_agent import BrowserAgentService

from ...domain.types._types import PartnerResult
from .notification import (
    NotificationService,
    OfferPositionChange,
)

from libs.domain.types._types.shared import APIClients

from libs.infrastructure.clients.http.schemas import (
    FetchLinks,
    FetchOffer,
    FetchOfferPosition,
    InsertOfferPosition,
    InsertPartner,
    InsertUTMSource,
    UpdateLink,
    UpdatePartner,
)


class ParserAgentService:
    def __init__(
        self,
        browser_agent: BrowserAgentService,
        api_clients: APIClients,
        notification_service: NotificationService,
    ) -> None:
        self._browser_agent = browser_agent
        self._api_clients = api_clients
        self._notification_service = notification_service
        self._default_offers: list[FetchOffer] | None = None

    async def aclose(self) -> None:
        await self._api_clients.close()
        await self._browser_agent.aclose()
        await self._notification_service.aclose()

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

    @staticmethod
    def _normalize_title(
        title: str,
    ) -> str:
        return title.strip().lower()

    async def _bind_link_offers(
        self,
        *,
        link: FetchLinks,
        result: PartnerResult,
        all_offers: list[FetchOffer],
    ) -> None:
        found_titles = {
            self._normalize_title(offer.title)
            for offer in result.target_offers_found
            if offer.is_found
        }

        if not found_titles:
            return

        offers_by_title = {
            self._normalize_title(offer.title): offer
            for offer in all_offers
        }
        offers_by_symbol = {
            offer.symbol: offer
            for offer in all_offers
            if offer.symbol
        }

        current_offer_ids = {
            offers_by_symbol[symbol].id
            for symbol in link.offers
            if symbol in offers_by_symbol
        }
        next_offer_ids = set(current_offer_ids)

        for title in found_titles:
            offer = offers_by_title.get(title)
            if offer:
                next_offer_ids.add(offer.id)

        if next_offer_ids == current_offer_ids:
            return

        await self._api_clients.link.update(
            link.id,
            UpdateLink(
                offer_ids=sorted(next_offer_ids),
            ),
        )

        logger.info(
            "Linked offers to link: link={} offer_ids={}",
            link.link,
            sorted(next_offer_ids),
        )

    async def _fetch_latest_offer_position(
        self,
        *,
        wmid: str,
        utm_source: str,
        vitrina: str,
        offer: str,
    ) -> FetchOfferPosition | None:
        positions = await self._api_clients.offer_position.fetch_all(
            filters={
                "wmid": wmid,
                "utm_source": utm_source,
                "vitrina": vitrina,
                "offer": offer,
            },
        )

        if not positions:
            return None

        return max(
            positions,
            key=lambda position: position.created_at or datetime.min,
        )

    async def _notify_position_change(
        self,
        *,
        previous: FetchOfferPosition | None,
        current: InsertOfferPosition,
    ) -> None:
        if (
            previous is None
            or previous.position is None
            or current.position is None
            or previous.position == current.position
            or not current.wmid
            or not current.utm_source
            or not current.offer
        ):
            return

        await self._notification_service.send_offer_position_changed(
            OfferPositionChange(
                wmid=current.wmid,
                utm_source=current.utm_source,
                vitrina=current.vitrina,
                offer=current.offer,
                previous_position=previous.position,
                current_position=current.position,
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

            previous_position = await self._fetch_latest_offer_position(
                wmid=wmid,
                utm_source=utm_source,
                vitrina=link.link,
                offer=offer.title,
            )

            current_position = InsertOfferPosition(
                wmid=wmid,
                utm_source=utm_source,
                offer=offer.title,
                vitrina=link.link,
                position=offer.position,
                created_at=datetime.now(),
            )

            await self._api_clients.offer_position.create(current_position)
            await self._notify_position_change(
                previous=previous_position,
                current=current_position,
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

            await self._bind_link_offers(
                link=link,
                result=result,
                all_offers=all_offers,
            )

            await self._persist_scan_result(
                link=link,
                result=result,
            )

            results.append(result)

        return results
