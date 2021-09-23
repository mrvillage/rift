from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

import discord
from discord.ext import commands

from src.data.query.target import add_target, remove_target

from ...cache import cache
from ...errors import TargetNotFoundError

__all__ = ("Target",)

if TYPE_CHECKING:
    from typings import TargetData

    from .nation import Nation


class Target:
    __slots__ = (
        "id",
        "target_id",
        "owner_id",
        "channel_ids",
        "role_ids",
        "user_ids",
        "direct_message",
    )

    def __init__(self, data: TargetData) -> None:
        self.id: int = data["id"]
        self.target_id: int = data["target_id"]
        self.owner_id: int = data["owner_id"]
        self.channel_ids: List[int] = data["channel_ids"]
        self.role_ids: List[int] = data["role_ids"]
        self.user_ids: List[int] = data["user_ids"]
        self.direct_message: bool = data["direct_message"]

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str, /) -> Target:
        try:
            return await cls.fetch(int(argument), ctx.author.id)
        except ValueError:
            raise TargetNotFoundError(argument)

    @classmethod
    async def fetch(cls, target_id: int, owner_id: int, /) -> Target:
        target = cache.get_target(target_id, owner_id)
        if target is None:
            raise TargetNotFoundError(target_id)
        return target

    def _update(self, data: TargetData) -> None:
        self.id: int = data["id"]
        self.target_id: int = data["target_id"]
        self.owner_id: int = data["owner_id"]
        self.channel_ids: List[int] = data["channel_ids"]
        self.role_ids: List[int] = data["role_ids"]
        self.user_ids: List[int] = data["user_ids"]

    def __int__(self) -> int:
        return self.id

    @property
    def mentions(self) -> str:
        return (
            " ".join(f"<@&{i}>" for i in self.role_ids)
            + " "
            + " ".join(f"<@{i}>" for i in self.user_ids)
        )

    @property
    def nation(self) -> Optional[Nation]:
        return cache.get_nation(self.target_id)

    @classmethod
    async def add(
        cls,
        target: Nation,
        owner: Union[discord.User, discord.Member],
        channels: List[discord.TextChannel],
        roles: List[discord.Role],
        users: List[Union[discord.User, discord.Member]],
        direct_message: bool = False,
        /,
    ) -> Target:
        data = await add_target(
            target.id,
            owner.id,
            [i.id for i in channels],
            [i.id for i in roles],
            [i.id for i in users],
            direct_message,
        )
        added = cls(data)
        cache._targets[added.id] = added
        return added

    async def remove(self) -> None:
        await remove_target(self.id)
        del cache._targets[self.id]
