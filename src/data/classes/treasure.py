from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ...cache import cache
from ...errors import TreasureNotFoundError
from ...ref import RiftContext

__all__ = ("Treasure",)

if TYPE_CHECKING:
    from _typings import TreasureData

    from .nation import Nation


class Treasure:
    __slots__ = ("name", "color", "_continent", "bonus", "spawn_date", "nation_id")

    def __init__(self, data: TreasureData, /):
        self.name: str = data["name"]
        self.color: str = data["color"]
        self._continent: str = data["continent"]
        self.bonus: int = data["bonus"]
        self.spawn_date: str = data["spawndate"]
        self.nation_id: int = int(data["nation"])

    @classmethod
    async def fetch(cls, ctx: RiftContext, name: str, /):
        treasure = cache.get_treasure(name)
        if treasure:
            return treasure
        raise TreasureNotFoundError(name)

    def update(self, data: TreasureData, /):
        self.name = data["name"]
        self.color = data["color"]
        self._continent = data["continent"]
        self.bonus = data["bonus"]
        self.spawn_date = data["spawndate"]
        self.nation_id = int(data["nation"])

    @property
    def nation(self) -> Optional[Nation]:
        return cache.get_nation(self.nation_id)
