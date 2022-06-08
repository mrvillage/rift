from __future__ import annotations

import asyncio
import datetime
import sys
import traceback
from functools import reduce
from typing import TYPE_CHECKING

import quarrel

__all__ = (
    "print_exception_with_header",
    "print_exception",
    "return_exception",
    "sleep_until",
    "utcnow",
    "default_missing",
    "default_none",
    "default_true",
    "default_false",
    "snake_case_to_capitals",
    "unique",
    "sort_models_by_id",
)

if TYPE_CHECKING:
    from typing import Any, Callable, Coroutine, Iterable, Optional, Protocol, TypeVar

    T = TypeVar("T")

    class IDProtocol(Protocol):
        id: int

    M = TypeVar("M", bound=IDProtocol)


def print_exception_with_header(header: str, error: Exception) -> None:
    print(header, file=sys.stderr)
    print_exception(error)


def print_exception(error: Exception) -> None:
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


async def return_exception(coro: Coroutine[Any, Any, T]) -> Exception | T:
    try:
        return await coro
    except Exception as e:
        return e


async def sleep_until(until: float) -> None:
    until -= utcnow().timestamp()
    if until <= 0:
        return
    await asyncio.sleep(until)


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)


def default_missing(*_: Any) -> Any:
    return quarrel.MISSING


def default_none(*_: Any) -> Any:
    return None


def default_true(*_: Any) -> bool:
    return True


def default_false(*_: Any) -> bool:
    return False


def snake_case_to_capitals(value: str) -> str:
    return " ".join(i.capitalize() for i in value.split("_"))


def unique(iterable: Iterable[T]) -> list[T]:
    return reduce(lambda a, b: a if b in a else a + [b], iterable, [])  # type: ignore


def sort_models_by_id(
    iterable: Iterable[M], predicate: Optional[Callable[[M], bool]] = None
) -> list[M]:
    predicate = predicate or (lambda _: True)
    return sorted((i for i in iterable if predicate(i)), key=lambda i: i.id)
