from __future__ import annotations

from typing import TypedDict

__all__ = ("AuditCheck",)


class AuditCheck(TypedDict):
    id: int
    name: str
    config_id: int
    condition: str
    fail_message_format: str
    success_message_format: str
    required: bool
    city: bool
