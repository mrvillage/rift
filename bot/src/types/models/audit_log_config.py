from __future__ import annotations

from typing import TypedDict

__all__ = ("AuditLogConfig",)


class AuditLogConfig(TypedDict):
    id: int
    guild_id: int
    channel_id: int
    target_guild_id: int
    target_alliance_id: int
    actions: list[int]
