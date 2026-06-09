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
        )

    def orm_model_dump(
        self,
    ) -> dict[str, Any]:
        columns = self._table.__table__.columns.keys()

        return {key: value for key, value in self.dump.items() if key in columns}
