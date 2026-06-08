# packages

from pydantic import Field

# application depencies

from libs.domain.types._types.common import BaseModelType


class Offer(BaseModelType):
    title: str = Field(
        default="",
        description="Название МФО оффера, например, 'Займер', 'Webbankir'",
    )

    position: int = Field(
        default=0,
        description="Порядковый номер карточки на сайте (сверху вниз)",
    )

    is_found: bool = Field(
        default=False,
        description="Бинарное значение, указывающее найден ли оффер",
    )
