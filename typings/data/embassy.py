from __future__ import annotations

from typing import Optional, TypedDict

__all__ = ("EmbassyData", "EmbassyConfigData")


class EmbassyData(TypedDict):
    embassy_id: int
    alliance_id: int
    channel_id: int
    config_id: int
    guild_id: int
    user_id: int
    open: bool


class EmbassyConfigData(TypedDict):
    config_id: int
    category_id: Optional[int]
    guild_id: int
    start_message: str
