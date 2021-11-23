from __future__ import annotations

from typing import TypedDict

__all__ = ("Permission",)


class Permission(TypedDict):
    name: str
    value: str
    description: str
    flag: int
