from typing import TypeVar

from libs.domain.types._types.common import BaseModelType


TList = TypeVar(
    "TList",
    bound=BaseModelType,
)

TDetail = TypeVar(
    "TDetail",
    bound=BaseModelType,
)
