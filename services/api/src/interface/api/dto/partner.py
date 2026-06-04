# packages

from pydantic import Field

from typing import Optional

# application dependencies

from .link import FetchLinks

from .base import BaseFetch

from libs.domain.types._types.common import BaseModelType


class BasePartner(BaseModelType):
    title: str = Field(
        ...,
        description="Название оффера",
    )


class FetchPartners(
    BasePartner,
    BaseFetch,
):
    is_tracking: bool = Field(
        default=True,
        description="Активность оффера",
    )

    links: Optional[list[FetchLinks]] = Field(
        default=list,
        description="Офферы, относящиеся к партнеру",
    )


class FetchPartner(
    BasePartner,
    BaseFetch,
):
    pass


class InsertPartner(BasePartner):
    is_tracking: bool = Field(
        default=True,
        description="Активность оффера",
    )

    link_ids: Optional[list[int]] = Field(
        default=list,
        description="ID офферов, относящихся к партнеру",
    )
