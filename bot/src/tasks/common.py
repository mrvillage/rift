from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING

from .. import utils

__all__ = ("CommonTask",)

if TYPE_CHECKING:
    ...


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
        ...

    def start(self) -> None:
        asyncio.create_task(self.run())

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
