from __future__ import annotations

from typing import TYPE_CHECKING

from ...cache import cache
from ...errors import ColorNotFoundError

__all__ = ("Color",)

if TYPE_CHECKING:
    from typings import ColorData


class Color:
    __slots__ = ("color", "name", "bonus")

    def __init__(self, data: ColorData) -> None:
        self.color: str = data["color"]
        self.name: str = data["bloc_name"]
        self.bonus: int = data["turn_bonus"]

    @classmethod
    async def fetch(cls, name: str, /) -> Color:
        color = cache.get_color(name)
        if color:
            return color
        raise ColorNotFoundError(name)

    def _update(self, data: ColorData) -> None:
        self.color = data["color"]
        self.name = data["bloc_name"]
        self.bonus = data["turn_bonus"]
