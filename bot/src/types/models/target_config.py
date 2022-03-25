from __future__ import annotations

from typing import TypedDict

__all__ = ("TargetConfig",)


class TargetConfig(TypedDict):
    id: int
    owner_id: int
    name: str
    count: int
    rater: int
    condition: str
    use_condition: str
    attack: bool
    public: bool
