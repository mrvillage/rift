from __future__ import annotations

from typing import Optional, TypedDict

__all__ = ("AccountData",)


class AccountData(TypedDict):
    id: int
    name: str
    owner: int
    alliance: int
    resources: str
    war_chest: bool
    primary_: bool
    deposit_code: Optional[str]
