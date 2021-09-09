from __future__ import annotations

from typing import Dict, List, Optional, TypedDict

__all__ = ("GuildSettingsData", "GuildWelcomeSettingsData")


class GuildSettingsData(TypedDict):
    guild_id: int


class GuildWelcomeSettingsData(TypedDict):
    guild_id: int
    welcome_message: str
    welcome_channels: Optional[List[int]]
    join_roles: Optional[List[int]]
    verified_roles: Optional[List[int]]
    member_roles: Optional[List[int]]
    global_city_roles: Optional[Dict[str, List[int]]]
    member_city_roles: Optional[Dict[str, List[int]]]
    diplomat_roles: Optional[Dict[str, List[int]]]
    alliance_roles: Optional[Dict[str, List[int]]]
    alliance_gov_roles: Optional[Dict[str, List[int]]]
    verified_nickname: Optional[str]
