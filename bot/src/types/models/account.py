from __future__ import annotations

from typing import TypedDict

from ..resources import Resources

__all__ = ("Account",)


class Account(TypedDict):
    id: int
    name: str
    owner_id: int
    alliance_id: int
    resources: Resources
    war_chest: bool
    primary: bool
    deposit_code: str
