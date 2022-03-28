from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("AuditRun",)

if TYPE_CHECKING:
    from typing import ClassVar

    from ...types.models.audit.audit_run import AuditRun as AuditRunData
    from ...types.models.audit.audit_run import AuditRunCheck


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class AuditRun:
    TABLE: ClassVar[str] = "audit_runs"
    id: int
    config_id: int
    nation_id: int
    checks: list[AuditRunCheck]

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: AuditRunData) -> AuditRun:
        ...

    def to_dict(self) -> AuditRunData:
        ...

    def update(self, data: AuditRun) -> AuditRun:
        ...
