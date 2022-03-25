from __future__ import annotations

from typing import TypedDict

__all__ = ("TicketConfig",)


class TicketConfig(TypedDict):
    id: int
    name: str
    category_id: int
    guild_id: int
    message: str
    archive_category_id: int
    mention_ids: list[int]
    default: bool
    name_format: str
    interview_config_id: int
