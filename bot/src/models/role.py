from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, flags, utils

__all__ = ("Role",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Role:
    TABLE: ClassVar[str] = "roles"
    id: int
    name: str
    description: str
    alliance_id: int
    rank: int
    permissions: flags.RolePermissions = attrs.field(converter=flags.RolePermissions)
    member_ids: list[int]
    role_ids: list[int]
    alliance_positions: list[int]
    privacy_level: int
    access_level: enums.AccessLevel = attrs.field(converter=enums.AccessLevel)

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Role:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: Role) -> Role:
        ...
