from __future__ import annotations

from typing import Any, List, Optional, TypedDict

__all__ = ("ConditionData",)


class ConditionData(TypedDict):
    id: int
    name: Optional[str]
    owner: Optional[int]
    condition: List[Any]
