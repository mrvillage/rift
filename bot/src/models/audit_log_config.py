from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import enums, utils

__all__ = ("AuditLogConfig",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ..types.models.audit_log_config import AuditLogConfig as AuditLogConfigData


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

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: AuditLogConfigData) -> AuditLogConfig:
        ...

    def to_dict(self) -> AuditLogConfigData:
        ...
