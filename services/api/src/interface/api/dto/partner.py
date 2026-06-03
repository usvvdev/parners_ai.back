from pydantic import Field

from typing import Optional

from .link import FetchLink

from .base import BaseFetch

from libs.domain.types._types.common import BaseModelType


class BasePartner(BaseModelType):
    title: str = Field(
        ...,
        description="Название оффера",
    )

    is_tracking: bool = Field(
        default=True,
        description="Активность оффера",
    )


class FetchPartnerLinks(
    BaseFetch,
    BasePartner,
):
    links: Optional[list[FetchLink]] = Field(
        default=list,
        description="Офферы, относящиеся к партнеру",
    )


class FetchPartner(
    BaseFetch,
    BasePartner,
):
    pass


class InsertPartner(BasePartner):
    link_ids: Optional[list[int]] = Field(
        default=list,
        description="ID офферов, относящихся к партнеру",
    )
