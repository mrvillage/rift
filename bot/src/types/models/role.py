from __future__ import annotations

from typing import TypedDict

__all__ = ("Role",)


class Role(TypedDict):
    id: int
    name: str
    description: str
    alliance_id: int
    rank: int
    permissions: int
    member_ids: list[int]
    role_ids: list[int]
    alliance_positions: list[int]
    privacy_level: int
    access_level: int
