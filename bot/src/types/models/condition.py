from __future__ import annotations

from typing import TypedDict

__all__ = ("Condition",)


class Condition(TypedDict):
    id: int
    name: str
    owner_id: int
    value: str
    public: bool
    use_condition: str
