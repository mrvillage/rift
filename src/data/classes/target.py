from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

import discord

from ...cache import cache
from ...errors import TargetNotFoundError
from ...funcs.utils import convert_int
from ...ref import RiftContext
from ..query import add_target_reminder, remove_target_reminder

__all__ = ("TargetReminder",)

if TYPE_CHECKING:
    from _typings import TargetReminderData

    from .nation import Nation


class TargetReminder:
    __slots__ = (
        "id",
        "target_id",
        "owner_id",
        "channel_ids",
        "role_ids",
        "user_ids",
        "direct_message",
    )

    def __init__(self, data: TargetReminderData) -> None:
        self.id: int = data["id"]
        self.target_id: int = data["target_id"]
        self.owner_id: int = data["owner_id"]
        self.channel_ids: List[int] = data["channel_ids"]
        self.role_ids: List[int] = data["role_ids"]
        self.user_ids: List[int] = data["user_ids"]
        self.direct_message: bool = data["direct_message"]

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str, /) -> TargetReminder:
        try:
            return await cls.fetch(convert_int(argument), ctx.author.id)
        except ValueError:
            raise TargetNotFoundError(argument)

    @classmethod
    async def fetch(cls, reminder_id: int, owner_id: int, /) -> TargetReminder:
        reminder = cache.get_target_reminder(reminder_id, owner_id)
        if reminder is None:
            raise TargetNotFoundError(reminder_id)
        return reminder

    def _update(self, data: TargetReminderData) -> None:
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
        nation: Nation,
        owner: Union[discord.User, discord.Member],
        channels: List[discord.TextChannel],
        roles: List[discord.Role],
        users: List[Union[discord.User, discord.Member]],
        direct_message: bool = False,
        /,
    ) -> TargetReminder:
        data = await add_target_reminder(
            nation.id,
            owner.id,
            [i.id for i in channels],
            [i.id for i in roles],
            [i.id for i in users],
            direct_message,
        )
        added = cls(data)
        cache.add_target_reminder(added)
        return added

    async def remove(self) -> None:
        await remove_target_reminder(self.id)
        cache.remove_target_reminder(self)
