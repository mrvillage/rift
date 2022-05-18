from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, utils

__all__ = ("AuditLog",)

if TYPE_CHECKING:
    from typing import Any, Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class AuditLog:
    TABLE: ClassVar[str] = "audit_logs"
    id: int
    config_id: int
    guild_id: int
    channel_id: int
    user_id: int
    alliance_id: int
    action: enums.AuditLogAction = attrs.field(converter=enums.AuditLogAction)
    data: dict[str, Any]

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AuditLog:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: AuditLog) -> AuditLog:
        ...
