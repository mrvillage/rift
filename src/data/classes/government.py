from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional

from ...cache import cache
from .alliance import Alliance
from .role import Role

__all__ = ("GovernmentDepartment",)


if TYPE_CHECKING:
    from _typings import GovernmentDepartmentData


class GovernmentDepartment:
    __slots__ = (
        "id",
        "name",
        "description",
        "alliance_id",
        "role_ids",
        "role_rankings",
        "parent_id",
    )

    def __init__(self, data: GovernmentDepartmentData) -> None:
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: Optional[str] = data["description"]
        self.alliance_id: int = data["alliance"]
        self.role_ids: List[int] = data["roles"]
        self.role_rankings: Dict[int, List[int]] = data["role_rankings"]
        self.parent_id: Optional[int] = data["parent"]

    @property
    def alliance(self) -> Optional[Alliance]:
        return cache.get_alliance(self.alliance_id)

    @property
    def roles(self) -> List[Role]:
        return [r for i in self.role_ids if (r := cache.get_role(i))]

    @property
    def parent(self) -> Optional[GovernmentDepartment]:
        return (
            cache.get_government_department(self.parent_id) if self.parent_id else None
        )
