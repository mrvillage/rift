from __future__ import annotations

from typing import List, Optional, TypedDict

__all__ = (
    "AllianceSettingsData",
    "GuildSettingsData",
    "GuildWelcomeSettingsData",
    "AllianceAutoRoleData",
)


class AllianceSettingsData(TypedDict):
    alliance: int
    default_raid_condition: Optional[str]
    default_nuke_condition: Optional[str]
    default_military_condition: Optional[str]
    default_attack_raid_condition: Optional[str]
    default_attack_nuke_condition: Optional[str]
    default_attack_military_condition: Optional[str]
    withdraw_channels: Optional[List[int]]
    require_withdraw_approval: bool
    offshore: Optional[int]
    withdraw_from_offshore: bool


class GuildSettingsData(TypedDict):
    guild: int
    purpose: Optional[str]
    purpose_argument: Optional[str]
    manager_role_ids: Optional[List[int]]


class GuildWelcomeSettingsData(TypedDict):
    guild: int
    welcome_message: Optional[str]
    welcome_channels: Optional[List[int]]
    join_roles: Optional[List[int]]
    verified_roles: Optional[List[int]]
    member_roles: Optional[List[int]]
    diplomat_roles: Optional[List[int]]
    verified_nickname: Optional[str]
    enforce_verified_nickname: Optional[bool]
    alliance_auto_roles_enabled: Optional[bool]
    alliance_auto_role_creation_enabled: Optional[bool]


class AllianceAutoRoleData(TypedDict):
    role: int
    guild: int
    alliance: int
