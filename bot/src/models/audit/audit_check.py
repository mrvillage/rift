from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("AuditCheck",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.audit.audit_check import AuditCheck as AuditCheckData


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

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: AuditCheckData) -> AuditCheck:
        ...

    def to_dict(self) -> AuditCheckData:
        ...

    def update(self, data: AuditCheck) -> AuditCheck:
        ...
