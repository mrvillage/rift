from __future__ import annotations

from typing import TypedDict

__all__ = ("InterviewConfig",)


class InterviewConfig(TypedDict):
    id: int
    name: str
    guild_id: int
