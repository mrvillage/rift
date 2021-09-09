from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Union

from ..query import query_color

__all__ = ("Color",)

if TYPE_CHECKING:
    from typings import ColorData


class Color:
    color: str
    name: str
    bloc_name: str
    bonus: int
    turn_bonus: int

    __slots__ = ("color", "name", "bloc_name", "bonus", "turn_bonus")

    def __init__(self, data: ColorData) -> None:
        self.color = data["color"]
        self.name = data["bloc_name"]
        self.bloc_name = self.name
        self.bonus = data["turn_bonus"]
        self.turn_bonus = self.bonus

    @classmethod
    async def fetch(cls, name: str) -> Color:
        return cls(await query_color(name))

    def _update(self, data, /) -> Color:
        ...
