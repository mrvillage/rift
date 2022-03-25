from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("WarRoom",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.war_room import WarRoom as WarRoomData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class WarRoom:
    TABLE: ClassVar[str] = "war_rooms"
    id: int
    config_id: int
    guild_id: int
    channel_id: int
    nation_id: int
    war_ids: list[int]
    archived: bool
    thread: bool

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: WarRoomData) -> WarRoom:
        ...
