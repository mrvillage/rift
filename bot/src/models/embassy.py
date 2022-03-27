from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Embassy",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.embassy import Embassy as EmbassyData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Embassy:
    TABLE: ClassVar[str] = "embassies"
    id: int
    config_id: int
    guild_id: int
    channel_id: int
    alliance_id: int
    archived: bool

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: EmbassyData) -> Embassy:
        ...

    def to_dict(self) -> EmbassyData:
        ...

    def update(self, data: Embassy) -> Embassy:
        ...
