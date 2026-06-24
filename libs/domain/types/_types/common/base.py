from typing import Any


class BasePydanticModel:
    @property
    def dump(
        self,
    ) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json",
            exclude_unset=True,
        )
