# packages

from typing import Optional

from pydantic import Field

# application depencies

from .base import BaseFetch

from .link import FetchLinks

from libs.domain.types._types.common import BaseModelType


class BasePartnerFields(BaseModelType):
    is_tracking: bool = Field(
        default=True,
        description="Статус трекинга",
    )

    is_selected: bool = Field(
        default=False,
        description="Избранный партнер",
    )


class PartnerIdentity(BaseModelType):
    wmid: str = Field(
        ...,
        description="WMID вебмастера",
    )

    utm_source: str = Field(
        ...,
        description="UTM-источник партнера",
    )


class FetchPartner(
    PartnerIdentity,
    BasePartnerFields,
    BaseFetch,
):
    pass


class FetchPartners(FetchPartner):
    links: list[FetchLinks] = Field(
        default_factory=list,
        description="Ссылки партнера",
    )


class InsertPartner(
    PartnerIdentity,
    BasePartnerFields,
):
    link_ids: list[int] = Field(
        default_factory=list,
        description="ID ссылок партнера",
    )


class UpdatePartner(BasePartnerFields):
    link_ids: Optional[list[int]] = Field(
        default=None,
        description="ID ссылок партнера",
    )
