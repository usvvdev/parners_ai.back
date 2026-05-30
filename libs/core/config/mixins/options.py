# packages

from pydantic import Field

from typing import Optional

# application dependencies

from libs.domain.types._types.options import EngineOptions


class ApplicationOptionsMixin:
    engine_options: Optional[EngineOptions] = Field(
        default=None,
        description="Engine connection options",
    )
