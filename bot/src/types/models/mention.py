from __future__ import annotations

from typing import TypedDict

__all__ = ("Mention",)


class Mention(TypedDict):
    id: int
    owner_id: int
    owner_type: int
    channel_ids: list[int]
    role_ids: list[int]
    user_ids: list[int]
