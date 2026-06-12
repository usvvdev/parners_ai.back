# packages

from pydantic import (
    Field,
    field_validator,
)

from typing import Optional

from datetime import datetime

from fastapi_pagination import Page

# application dependencies

from .link import FetchLinks

from .utm_source import FetchUTMSource

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


class FetchPartners(
    PartnerIdentity,
    BasePartnerFields,
    BaseFetch,
):
    utm_source: Optional[FetchUTMSource | str] = Field(
        default=None,
        description="UTM метка",
    )

    links: Optional[Page[FetchLinks]] = Field(
        default=None,
        description="Офферы, относящиеся к партнеру",
    )

    @field_validator("utm_source", mode="after")
    def validate_utm_source(
        cls,
        value: Optional[FetchUTMSource],
    ) -> str:
        if value is not None:
            return value.title
        return value


class FetchPartner(
    PartnerIdentity,
    BasePartnerFields,
    BaseFetch,
):
    utm_source: Optional[FetchUTMSource | str] = Field(
        default=None,
        description="UTM метка",
    )

    @field_validator("utm_source", mode="after")
    def validate_utm_source(
        cls,
        value: Optional[FetchUTMSource],
    ) -> str:
        if value is not None:
            return value.title
        return value


class InsertPartner(
    PartnerIdentity,
    BasePartnerFields,
):
    utm_source_id: int = Field(
        ...,
        description="Название оффера",
    )

    link_ids: list[int] = Field(
        default_factory=list,
        description="ID офферов, относящихся к партнеру",
    )


class UpdatePartner(BasePartnerFields):
    link_ids: Optional[list[int]] = Field(
        default=None,
        description="ID офферов, относящихся к партнеру",
    )

    updated_at: datetime = Field(
        default=datetime.now(),
        description="Текущее время обновления",
    )
