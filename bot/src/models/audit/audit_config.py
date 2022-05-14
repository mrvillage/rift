from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("AuditConfig",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


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

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AuditConfig:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: AuditConfig) -> AuditConfig:
        ...
