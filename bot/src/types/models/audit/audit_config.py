from __future__ import annotations

from typing import TypedDict

__all__ = ("AuditConfig",)


class AuditConfig(TypedDict):
    id: int
    name: str
    alliance_id: int
    fail_message_format: str
    success_message_format: str
