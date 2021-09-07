from __future__ import annotations
from typing import Dict, TYPE_CHECKING, Union

from ..query import query_color

__all__ = ("Color",)


class Color:
    data: Dict[str, Union[int, str]]
    color: str
    name: str
    bloc_name: str
    bonus: int
    turn_bonus: int

    __slots__ = ("data", "color", "name", "bloc_name", "bonus", "turn_bonus")

    def __init__(self, data: Dict[str, Union[int, str]]) -> None:
        if TYPE_CHECKING:
            assert (
                isinstance(data["color"], str)
                and isinstance(data["bloc_name"], str)
                and isinstance(data["turn_bonus"], int)
            )
        self.data = data
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
