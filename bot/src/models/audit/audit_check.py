from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("AuditCheck",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class AuditCheck:
    TABLE: ClassVar[str] = "audit_checks"
    id: int
    name: str
    config_id: int
    condition: str
    fail_message_format: str
    success_message_format: str
    required: bool
    city: bool

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AuditCheck:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: AuditCheck) -> AuditCheck:
        ...
