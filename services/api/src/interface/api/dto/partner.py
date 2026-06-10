# packages

from pydantic import Field

from typing import Optional

# application dependencies

from .link import FetchLinks

from .base import BaseFetch

from libs.domain.types._types.common import BaseModelType


class BasePartnerFields(BaseModelType):
    is_tracking: bool = Field(
        default=True,
        description="Активность оффера",
    )


class PartnerIdentity(BaseModelType):
    wmid: str = Field(
        ...,
        description="Название оффера",
    )

    utm_source: str = Field(
        ...,
        description="Название оффера",
    )


class FetchPartners(
    PartnerIdentity,
    BasePartnerFields,
    BaseFetch,
):
    links: list[FetchLinks] = Field(
        default_factory=list,
        description="Офферы, относящиеся к партнеру",
    )


class FetchPartner(
    PartnerIdentity,
    BasePartnerFields,
    BaseFetch,
):
    pass


class InsertPartner(
    PartnerIdentity,
    BasePartnerFields,
):
    link_ids: list[int] = Field(
        default_factory=list,
        description="ID офферов, относящихся к партнеру",
    )


class UpdatePartner(BasePartnerFields):
    link_ids: Optional[list[int]] = Field(
        default=None,
        description="ID офферов, относящихся к партнеру",
    )
