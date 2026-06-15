# packages

from pydantic import Field

from .base import BaseFetch


class FetchOffer(BaseFetch):
    title: str = Field(
        ...,
        description="Название оффера",
    )

    symbol: str = Field(
        default="",
        description="Символ оффера",
    )
