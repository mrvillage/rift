from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("WarRoomConfig",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class WarRoomConfig:
    TABLE: ClassVar[str] = "war_room_configs"
    id: int
    name: str
    channel_id: int
    category_ids: list[int]
    guild_id: int
    message: str
    mention_ids: list[int]
    name_format: str
    reuse: bool
    condition: str
    track_wars: bool
    advise: bool

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WarRoomConfig:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: WarRoomConfig) -> WarRoomConfig:
        ...
