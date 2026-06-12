# packages

from pydantic import Field

from typing import Optional

# application dependencies

from libs.domain.types._types.options import (
    EngineOptions,
    OpenAPIOptions,
    TelegramOptions,
)


class ApplicationOptionsMixin:
    engine_options: Optional[EngineOptions] = Field(
        default=None,
        description="Engine connection options",
    )

    openai_options: Optional[OpenAPIOptions] = Field(
        default_factory=OpenAPIOptions,
        description="Openai application options",
    )

    telegram_options: Optional[TelegramOptions] = Field(
        default=None,
        description="Telegram options",
    )
