from __future__ import annotations

from typing import TypedDict

__all__ = ("TargetReminder",)


class TargetReminder(TypedDict):
    id: int
    nation_id: int
    owner_id: int
    mention_ids: list[int]
    direct_message: bool
    times: list[int]
