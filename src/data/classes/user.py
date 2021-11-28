from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ("User",)

if TYPE_CHECKING:
    from _typings import UserData


class User:
    def __init__(self, data: UserData) -> None:
        self.user_id: int = data["user_id"]
        self.nation_id: int = data["nation_id"]
