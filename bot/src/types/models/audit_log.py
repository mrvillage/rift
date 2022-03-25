from __future__ import annotations

from typing import Any, TypedDict

__all__ = ("AuditLog",)


class AuditLog(TypedDict):
    id: int
    config_id: int
    guild_id: int
    channel_id: int
    user_id: int
    alliance_id: int
    action: int
    data: dict[str, Any]
