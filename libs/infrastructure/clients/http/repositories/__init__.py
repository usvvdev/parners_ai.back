from .link import LinkAPIClient

from .offer import OfferAPIClient

from .partner import PartnerAPIClient

from .utm_source import UTMSourceAPIClient

from .offer_position import OfferPositionAPIClient


CLIENTS = {
    "link": LinkAPIClient,
    "offer": OfferAPIClient,
    "partner": PartnerAPIClient,
    "utm_source": UTMSourceAPIClient,
    "offer_position": OfferPositionAPIClient,
}

__all__: list[str] = [
    "LinkAPIClient",
    "OfferAPIClient",
    "PartnerAPIClient",
    "UTMSourceAPIClient",
    "OfferPositionAPIClient",
    "CLIENTS",
]
