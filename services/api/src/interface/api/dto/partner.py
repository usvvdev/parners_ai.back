# packages

from pydantic import Field

from typing import Optional

from fastapi_pagination import Page

# application dependencies

from .link import FetchLinks

from .base import BaseFetch

from libs.domain.types._types.common import BaseModelType


class BasePartnerFields(BaseModelType):
    is_tracking: bool = Field(
        default=True,
        description="Активность оффера",
    )

    is_selected: bool = Field(
        default=False,
        description="Избранный партнер",
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
    links: Optional[Page[FetchLinks]] = Field(
        default=None,
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
