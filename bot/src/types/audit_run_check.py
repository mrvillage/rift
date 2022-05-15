from __future__ import annotations

from typing import TypedDict

__all__ = ("AuditRunCheck",)

class AuditRunCheck(TypedDict):
    check_id: int
    success: bool
