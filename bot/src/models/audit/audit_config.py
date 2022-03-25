from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("AuditConfig",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.audit.audit_config import AuditConfig as AuditConfigData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class AuditConfig:
    TABLE: ClassVar[str] = "audit_configs"
    id: int
    name: str
    alliance_id: int
    fail_message_format: str
    success_message_format: str

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: AuditConfigData) -> AuditConfig:
        ...
