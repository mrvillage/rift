from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING

from .. import utils

__all__ = ("CommonTask",)

if TYPE_CHECKING:
    from typing import TypeVar

    T = TypeVar("T", bound="CommonTask")


class CommonTask:
    def __init__(self, interval: float) -> None:
        self.interval: float = interval
        self.last_run: float = 0.0

    async def before_task(self) -> None:
        ...

    async def after_task(self) -> None:
        ...

    async def task(self) -> None:
        ...

    async def on_error(self, error: Exception) -> None:
        utils.print_exception_with_header(
            f"Ignoring exception in task {type(self).__name__}:", error
        )

    def start(self: T) -> T:
        asyncio.create_task(self.run())
        return self

    async def run(self) -> None:
        before = await utils.return_exception(self.before_task())
        if isinstance(before, Exception):
            await utils.return_exception(self.on_error(before))
            return
        while True:
            self.last_run = time.time()
            error = await utils.return_exception(self.task())
            if isinstance(error, Exception):
                await utils.return_exception(self.on_error(error))
            await utils.sleep_until(self.last_run + self.interval)
