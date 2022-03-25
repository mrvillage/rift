from __future__ import annotations

from typing import TypedDict

__all__ = ("GuildSettings",)


class GuildSettings(TypedDict):
    purpose: int
    purpose_argument: str
    public: bool
    description: str
    welcome_message: str
    welcome_channels: list[int]
    join_role_ids: list[int]
    verified_role_ids: list[int]
    member_role_ids: list[int]
    verified_nickname_format: str
    enforce_verified_nickname: bool
    welcome_mentions: list[int]
