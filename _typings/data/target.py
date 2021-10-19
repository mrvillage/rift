from __future__ import annotations

from typing import List, Optional, TypedDict

__all__ = (
    "TargetData",
    "TargetReminderData",
)


class TargetData(TypedDict):
    id: int
    resources: Optional[str]
    last_turn_fetched: Optional[str]
    resources_off_attack: bool


class TargetReminderData(TypedDict):
    id: int
    target_id: int
    owner_id: int
    channel_ids: List[int]
    role_ids: List[int]
    user_ids: List[int]
    direct_message: bool
