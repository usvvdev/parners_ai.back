# packages

from functools import cached_property

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from sqlalchemy.orm import sessionmaker

# application dependencies

from ..base import BaseEngine


class BaseSQLEngine(BaseEngine):
    @cached_property
    def engine(self) -> AsyncEngine:
        return create_async_engine(
            **self.options.model_dump(
                exclude=None,
            ),
        )

    @cached_property
    def session_factory(self) -> sessionmaker[AsyncSession]:
        return sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
