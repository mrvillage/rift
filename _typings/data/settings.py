from __future__ import annotations

from typing import List, Optional, TypedDict

__all__ = ("AllianceSettingsData", "GuildSettingsData", "GuildWelcomeSettingsData")


class AllianceSettingsData(TypedDict):
    alliance_id: int
    default_raid_condition: Optional[str]
    default_nuke_condition: Optional[str]
    default_military_condition: Optional[str]


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
    diplomat_roles: Optional[List[int]]
    verified_nickname: Optional[str]
    enforce_verified_nickname: Optional[bool]
