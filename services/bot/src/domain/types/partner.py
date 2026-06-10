# packages

from pydantic import Field

# application dependencies

from .link import LinkSummary

from libs.domain.types._types.common import BaseModelType


class Partner(BaseModelType):
    id: int = Field(
        ...,
        description="ID партнера",
    )

    wmid: str = Field(
        ...,
        description="WMID вебмастера",
    )

    utm_source: str = Field(
        ...,
        description="UTM-источник партнера",
    )

    is_tracking: bool = Field(
        ...,
        description="Статус трекинга",
    )

    is_selected: bool = Field(
        ...,
        description="В избранном",
    )


class PartnerDetail(Partner):
    links: list[LinkSummary] = Field(
        default_factory=list,
        description="Ссылки партнера",
    )
