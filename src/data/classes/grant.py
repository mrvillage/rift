from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

from ...cache import cache
from ...enums import GrantPayoff
from ...errors import GrantNotFoundError
from ...funcs.utils import convert_int
from ...ref import bot
from ..db import execute_query, execute_read_query
from .resources import Resources

__all__ = ("Grant",)

if TYPE_CHECKING:
    from typing import Union

    import discord

    from _typings import GrantData

    from ...ref import RiftContext


class Grant:
    __slots__ = (
        "id",
        "time",
        "recipient_id",
        "resources",
        "payoff",
        "note",
        "deadline",
        "paid",
    )

    def __init__(self, data: GrantData) -> None:
        self.id: int = data.get("id", 0)
        self.recipient_id: int = data["recipient"]
        self.time: datetime.datetime = datetime.datetime.fromisoformat(data["time"])
        self.resources: Resources = Resources.convert_resources(data["resources"])
        self.payoff: GrantPayoff = GrantPayoff(data["payoff"])
        self.note: Optional[str] = data["note"]
        self.deadline: Optional[datetime.datetime] = (
            datetime.datetime.fromisoformat(data["deadline"])
            if data["deadline"] is not None
            else None
        )
        self.paid: Resources = Resources.convert_resources(data["paid"])

    @property
    def recipient(self) -> Optional[discord.User]:
        return bot.get_user(self.recipient_id)

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str) -> Grant:
        try:
            grant = cache.get_grant(convert_int(argument))
            if grant is not None:
                return grant
        except ValueError:
            pass
        raise GrantNotFoundError(argument)

    @classmethod
    async def create(
        cls,
        recipient: Union[discord.Member, discord.User],
        time: datetime.datetime,
        resources: Resources,
        payoff: GrantPayoff,
        note: Optional[str],
        deadline: Optional[datetime.datetime],
        paid: Resources,
    ) -> Grant:
        grant = cls(
            {
                "id": 0,
                "recipient": recipient.id,
                "time": str(time),
                "resources": str(resources),
                "payoff": payoff.value,
                "note": note,
                "deadline": str(deadline) if deadline is not None else None,
                "paid": str(paid),
            }
        )
        await grant.save()
        return grant

    async def save(self) -> None:
        if self.id:
            await execute_query(
                "UPDATE grants SET recipient = $2, time = $3, resources = $4, payoff = $5, note = $6, deadline = $7 WHERE id = $1;",
                self.id,
                self.recipient_id,
                str(self.time),
                str(self.resources),
                self.payoff.value,
                self.note,
                str(self.deadline) if self.deadline is not None else None,
            )
        else:
            id = await execute_read_query(
                "INSERT INTO grants (recipient, time, resources, payoff, note, deadline) VALUES ($1, $2, $3, $4, $6) RETURNING id;",
                self.recipient_id,
                str(self.time),
                str(self.resources),
                self.payoff.value,
                self.note,
                str(self.deadline) if self.deadline is not None else None,
            )
            self.id = id[0]["id"]
            cache.add_grant(self)

    async def send(self) -> None:
