from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("BlitzTarget",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.blitz_target import BlitzTarget as BlitzTargetData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class BlitzTarget:
    TABLE: ClassVar[str] = "blitz_targets"
    id: int
    blitz_id: int
    war_room_id: int
    nation_id: int
    attacker_ids: list[int]

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: BlitzTargetData) -> BlitzTarget:
        ...

    def to_dict(self) -> BlitzTargetData:
        ...

    def update(self, data: BlitzTarget) -> BlitzTarget:
        ...
