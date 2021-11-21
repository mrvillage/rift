from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ...cache import cache
from ...flags import RolePermissions
from .alliance import Alliance

__all__ = ("Role",)

if TYPE_CHECKING:
    from _typings import RoleData


class Role:
    __slots__ = ("id", "name", "description", "alliance_id", "rank", "permissions")

    def __init__(self, data: RoleData) -> None:
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: Optional[str] = data["description"]
        self.alliance_id: int = data["alliance"]
        self.rank: int = data["rank"]
        self.permissions: RolePermissions = RolePermissions(data["permissions"])

    @property
    def alliance(self) -> Optional[Alliance]:
        return cache.get_alliance(self.alliance_id)
