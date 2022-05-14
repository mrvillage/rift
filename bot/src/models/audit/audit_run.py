from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from ... import utils

__all__ = ("AuditRun",)

if TYPE_CHECKING:
    from typing import Any, ClassVar


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
    def from_dict(cls, data: dict[str, Any]) -> AuditRun:
        ...

    def to_dict(self) -> dict[str, Any]:
        ...

    def update(self, data: AuditRun) -> AuditRun:
        ...
