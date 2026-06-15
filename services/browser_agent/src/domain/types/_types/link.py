# packages

from pydantic import Field, field_validator

from .base import BaseFetch


class FetchLinks(BaseFetch):
    link: str = Field(
        ...,
        description="URL витрины",
    )

    is_active: bool = Field(
        default=True,
        description="Активность витрины",
    )

    offers: list[str] = Field(
        default_factory=list,
        description="Символы офферов",
    )

    @field_validator("offers", mode="before")
    @classmethod
    def _normalize_offers(cls, v: list | None) -> list:
        return v if v is not None else []
