from __future__ import annotations

from typing import TypedDict

__all__ = ("ConditionalAutoRole",)


class ConditionalAutoRole(TypedDict):
    id: int
    role_id: int
    guild_id: int
    condition: str
