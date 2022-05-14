from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Embassy",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


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

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Embassy:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Embassy) -> Embassy:
        ...
