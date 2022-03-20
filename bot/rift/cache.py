from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from . import db

__all__ = ("cache",)

if TYPE_CHECKING:
    ...


class Cache:
    __slots__ = ()

    def __init__(self) -> None:
        ...

    async def initialize(self) -> None:
        info = []
        data = await asyncio.gather(
            *(db.query(f"SELECT * FROM {i['model'].TABLE};") for i in info)  # nosec
        )
        for i, result in zip(info, data):
            attr = getattr(self, f"_{i['model'].TABLE}")
            for row in result:
                # too lazy to properly type this
                model = i["model"].from_dict(row)  # type: ignore
                attr[i.key if hasattr(i, "key") else model.id] = model  # type: ignore

    def clear(self) -> None:
        ...


cache = Cache()
