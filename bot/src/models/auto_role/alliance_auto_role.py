from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import enums, utils

__all__ = ("AllianceAutoRole",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class AllianceAutoRole:
    TABLE: ClassVar[str] = "alliance_auto_roles"
    id: int
    role_id: int
    guild_id: int
    alliance_id: int
    access_level: enums.AccessLevel = attrs.field(converter=enums.AccessLevel)
    condition: str

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AllianceAutoRole:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: AllianceAutoRole) -> AllianceAutoRole:
        ...
