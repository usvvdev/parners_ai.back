# packages

from redis.asyncio import (
    Redis,
    from_url,
)

from functools import cached_property

# application dependencies

from ..base import BaseEngine


class BaseCacheEngine(BaseEngine):
    @cached_property
    def engine(self) -> Redis:
        return from_url(
            **self.options.dump,
        )
