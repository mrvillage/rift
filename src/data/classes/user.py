from __future__ import annotations

from typing import TYPE_CHECKING, Union

from ...cache import cache
from ..db import execute_query

__all__ = ("User",)

if TYPE_CHECKING:
    import discord

    from _typings import UserData

    from ..classes import Nation


class User:
    __slots__ = ("user_id", "nation_id")

    def __init__(self, data: UserData) -> None:
        self.user_id: int = data["user_"]
        self.nation_id: int = data["nation"]

    @classmethod
    async def create(
        cls, user: Union[discord.User, discord.Member], nation: Nation
    ) -> User:
        user_ = cls({"user_": user.id, "nation": nation.id})
        await user_.save()
        cache.add_user(user_)
        return user_

    async def save(self) -> None:
        await execute_query(
            "INSERT INTO users (user_, nation) VALUES ($1, $2) ON CONFLICT (user_) DO UPDATE SET user_ = $1, nation = $2;",
            self.user_id,
            self.nation_id,
        )

    async def delete(self) -> None:
        await execute_query(
            "UPDATE users SET nation = null WHERE user_ = $1;", self.user_id
        )
        cache.remove_user(self)
