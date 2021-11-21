from __future__ import annotations

from typing import Optional, TypedDict

__all__ = ("RoleData",)


class RoleData(TypedDict):
    id: int
    name: str
    description: Optional[str]
    alliance: int
    rank: int
    permissions: int
