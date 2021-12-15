from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from ...cache import cache
from ...enums import GrantPayoff
from ...errors import GrantNotFoundError
from ...funcs.utils import convert_int
from ..db import execute_query, execute_read_query
from .resources import Resources

__all__ = ("Grant",)

if TYPE_CHECKING:
    from typing import Union

    import discord

    from _typings import GrantData

    from ...ref import RiftContext


class Grant:
    __slots__ = ("id", "time", "recipient_id", "resources", "payoff")

    def __init__(self, data: GrantData) -> None:
        self.id: int = data.get("id", 0)
        self.recipient_id: int = data["recipient"]
        self.time: datetime.datetime = datetime.datetime.fromisoformat(data["time"])
        self.resources: Resources = Resources.convert_resources(data["resources"])
        self.payoff: GrantPayoff = GrantPayoff(data["payoff"])

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
    ) -> Grant:
        grant = cls(
            {
                "id": 0,
                "recipient": recipient.id,
                "time": str(time),
                "resources": str(resources),
                "payoff": payoff.value,
            }
        )
        await grant.save()
        return grant

    async def save(self) -> None:
        if self.id:
            await execute_query(
                "UPDATE transaction_requests SET recipient = $2, time = $3, resources = $4, payoff = $5 WHERE id = $1;",
                self.id,
                self.recipient_id,
                str(self.time),
                str(self.resources),
                self.payoff.value,
            )
        else:
            id = await execute_read_query(
                "INSERT INTO transaction_requests (recipient, time, resources, payoff) VALUES ($1, $2, $3, $4) RETURNING id;",
                self.recipient_id,
                str(self.time),
                str(self.resources),
                self.payoff.value,
            )
            self.id = id[0]["id"]
            cache.add_grant(self)
