# packages

from pydantic import Field

from libs.domain.types._types.shared import BaseFetchType

from libs.domain.types._types.common import BaseModelType


class UTMSourceIdentity(BaseModelType):
    title: str = Field(
        ...,
        description="Название UTM-источника",
    )


class FetchUTMSource(
    UTMSourceIdentity,
    BaseFetchType,
):
    title: str = Field(
        ...,
        description="Название UTM-источника",
    )


class FetchUTMSources(FetchUTMSource):
    pass


class InsertUTMSource(UTMSourceIdentity):
    pass
