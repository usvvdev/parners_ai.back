from pydantic import Field


class BaseFetch:
    id: int = Field(
        ...,
        description="ID оффера",
    )
