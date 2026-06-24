from typing import Any

from ..types._types.common import BaseModelType


def orm_model_dump(
    data: BaseModelType,
    table: Any,
) -> dict[str, Any]:
    columns = table.columns.keys()

    return {key: value for key, value in data.dump.items() if key in columns}
