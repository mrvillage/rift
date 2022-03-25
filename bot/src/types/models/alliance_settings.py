from __future__ import annotations

from typing import TypedDict

__all__ = ("AllianceSettings",)


class AllianceSettings(TypedDict):
    alliance_id: int
    default_raid_condition: str
    default_nuke_condition: str
    default_military_condition: str
    default_attack_raid_condition: str
    default_attack_nuke_condition: str
    default_attack_military_condition: str
    withdraw_channel_ids: list[int]
    require_withdraw_approval: bool
    offshore_id: int
    withdraw_from_offshore: bool
