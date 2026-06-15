# packages

from pydantic import Field

from .base import BaseFetch

from libs.domain.types._types.common import BaseModelType


class FetchUTMSource(BaseFetch):
    title: str = Field(
        ...,
        description="Название UTM-источника",
    )


class InsertUTMSource(BaseModelType):
    title: str = Field(
        ...,
        description="Название UTM-источника",
    )
