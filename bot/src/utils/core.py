from __future__ import annotations

import asyncio
import datetime
import time
from typing import TYPE_CHECKING

__all__ = ("return_exception", "sleep_until", "utcnow")

if TYPE_CHECKING:
    from typing import Any, Coroutine, TypeVar

    T = TypeVar("T")


async def return_exception(coro: Coroutine[Any, Any, T]) -> Exception | T:
    try:
        return await coro
    except Exception as e:
        return e


async def sleep_until(until: float) -> None:
    until -= time.time()
    if until <= 0:
        return
    await asyncio.sleep(until)


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)
