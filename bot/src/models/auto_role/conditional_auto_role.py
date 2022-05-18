from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("ConditionalAutoRole",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class ConditionalAutoRole:
    TABLE: ClassVar[str] = "conditional_auto_roles"
    id: int
    role_id: int
    guild_id: int
    condition: str

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConditionalAutoRole:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: ConditionalAutoRole) -> ConditionalAutoRole:
        ...
