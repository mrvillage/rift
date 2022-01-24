from __future__ import annotations

from typing import Optional, TypedDict

__all__ = ("ConditionData",)


class ConditionData(TypedDict):
    id: int
    name: Optional[str]
    owner: int
    condition: str
    public: bool
