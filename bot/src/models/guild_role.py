from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import flags, utils

__all__ = ("GuildRole",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class GuildRole:
    TABLE: ClassVar[str] = "guild_roles"
    id: int
    guild_id: int
    permissions: flags.GuildRolePermissions = attrs.field(
        converter=flags.GuildRolePermissions
    )

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GuildRole:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: GuildRole) -> GuildRole:
        ...
