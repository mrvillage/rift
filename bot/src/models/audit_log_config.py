from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, utils

__all__ = ("AuditLogConfig",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class AuditLogConfig:
    TABLE: ClassVar[str] = "audit_log_configs"
    id: int
    guild_id: int
    channel_id: int
    target_guild_id: int
    target_alliance_id: int
    actions: list[enums.AuditLogAction]

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AuditLogConfig:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: AuditLogConfig) -> AuditLogConfig:
        ...
