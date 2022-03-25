from __future__ import annotations

from typing import TypedDict

__all__ = ("AuditRun",)


class AuditRun(TypedDict):
    id: int
    config_id: int
    nation_id: int
    checks: AuditRunCheck


class AuditRunCheck(TypedDict):
    check_id: int
    success: bool
