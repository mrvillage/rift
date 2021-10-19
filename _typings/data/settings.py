from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict

__all__ = ("AllianceSettingsData", "GuildSettingsData", "GuildWelcomeSettingsData")


class AllianceSettingsData(TypedDict):
    alliance_id: int
    default_raid_condition: Optional[List[Any]]


class GuildSettingsData(TypedDict):
    guild_id: int
    purpose: Optional[str]
    purpose_argument: Optional[str]
    manager_role_ids: Optional[List[int]]


class GuildWelcomeSettingsData(TypedDict):
    guild_id: int
    welcome_message: Optional[str]
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
