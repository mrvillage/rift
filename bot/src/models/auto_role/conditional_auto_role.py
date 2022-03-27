from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("ConditionalAutoRole",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.auto_role.conditional_auto_role import (
        ConditionalAutoRole as ConditionalAutoRoleData,
    )


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class ConditionalAutoRole:
    TABLE: ClassVar[str] = "conditional_auto_roles"
    id: int
    role_id: int
    guild_id: int
    condition: str

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: ConditionalAutoRoleData) -> ConditionalAutoRole:
        ...

    def to_dict(self) -> ConditionalAutoRoleData:
        ...

    def update(self, data: ConditionalAutoRole) -> ConditionalAutoRole:
        ...
