from __future__ import annotations
from typing import Dict, TYPE_CHECKING, Union

from .base import Fetchable
from ..query import get_color


class Color(Fetchable):
    data: Dict[str, Union[int, str]]
    color: str
    name: str
    bloc_name: str
    bonus: int
    turn_bonus: int

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
        return cls(await get_color(name))
