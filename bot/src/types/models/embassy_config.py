from __future__ import annotations

from typing import TypedDict

__all__ = ("EmbassyConfig",)


class EmbassyConfig(TypedDict):
    id: int
    name: str
    category_id: int
    guild_id: int
    message: str
    archive_category_id: int
    mentions: list[int]
    default: bool
    name_format: str
    access_level: int
