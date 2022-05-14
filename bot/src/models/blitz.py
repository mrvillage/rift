from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Blitz",)

if TYPE_CHECKING:
    import datetime
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Blitz:
    TABLE: ClassVar[str] = "blitzes"
    id: int
    date: datetime.datetime
    name: str
    message: str
    alliance_ids: list[int]
    planning_alliance_ids: list[int]
    war_room_config: int
    direct_message: bool
    in_game_message: bool

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Blitz:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Blitz) -> Blitz:
        ...
