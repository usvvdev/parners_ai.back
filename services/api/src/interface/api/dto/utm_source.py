# packages

from pydantic import Field

# application dependencies

from .base import BaseFetch

from libs.domain.types._types.common import BaseModelType


class UTMSourceIdentity(BaseModelType):
    title: str = Field(
        ...,
        description="Название оффера",
    )


class FetchUTMSources(
    UTMSourceIdentity,
    BaseFetch,
):
    pass


class FetchUTMSource(
    UTMSourceIdentity,
    BaseFetch,
):
    pass


class InsertUTMSource(UTMSourceIdentity):
    pass


class UpdateUTMSource(UTMSourceIdentity):
    pass
