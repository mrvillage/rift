from __future__ import annotations

from typing import Dict, List, Optional, TypedDict

__all__ = ("GovernmentDepartmentData",)


class GovernmentDepartmentData(TypedDict):
    id: int
    name: str
    description: Optional[str]
    alliance: int
    roles: List[int]
    role_rankings: Dict[int, List[int]]
    parent: Optional[int]
