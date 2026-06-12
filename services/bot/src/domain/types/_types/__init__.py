from .base import (
    BaseFetch,
    PaginatedResponse,
)

from .offer import (
    FetchOffer,
    InsertOffer,
    UpdateOffer,
)

from .link import (
    FetchLinks,
    FetchLink,
    InsertLink,
    UpdateLink,
)

from .partner import (
    FetchPartner,
    FetchPartners,
    InsertPartner,
    UpdatePartner,
)

__all__: list[str] = [
    "BaseFetch",
    "PaginatedResponse",
    "FetchOffer",
    "InsertOffer",
    "UpdateOffer",
    "FetchLinks",
    "FetchLink",
    "InsertLink",
    "UpdateLink",
    "FetchPartner",
    "FetchPartners",
    "InsertPartner",
    "UpdatePartner",
]
