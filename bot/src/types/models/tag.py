from __future__ import annotations

from typing import TypedDict

__all__ = ("Tag",)


class Tag(TypedDict):
    id: int
    name: str
    owner_id: int
    message: str
    use_condition: str
