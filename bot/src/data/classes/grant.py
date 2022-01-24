from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

from ... import funcs
from ...cache import cache
from ...enums import (
    AccountType,
    GrantPayoff,
    GrantStatus,
    TransactionStatus,
    TransactionType,
)
from ...errors import GrantNotFoundError
from ...funcs.utils import convert_int
from ...ref import bot
from ..db import execute_query, execute_read_query
from .resources import Resources
from .transaction import Transaction

__all__ = ("Grant",)

if TYPE_CHECKING:
    from typing import Union

    import discord
    from _typings import GrantData

    from ...ref import RiftContext
    from .alliance import Alliance


class Grant:
    __slots__ = (
        "id",
        "time",
        "recipient_id",
        "resources",
        "alliance_id",
        "payoff",
        "note",
        "deadline",
        "paid",
        "status",
        "code",
    )

    def __init__(self, data: GrantData) -> None:
        self.id: int = data.get("id", 0)
        self.recipient_id: int = data["recipient"]
        self.time: datetime.datetime = datetime.datetime.fromisoformat(data["time"])
        self.resources: Resources = Resources.convert_resources(data["resources"])
        self.alliance_id: int = data["alliance"]
        self.payoff: GrantPayoff = GrantPayoff(data["payoff"])
        self.note: Optional[str] = data["note"]
        self.deadline: Optional[datetime.datetime] = (
            datetime.datetime.fromisoformat(data["deadline"])
            if data["deadline"] is not None
            else None
        )
        self.paid: Resources = Resources.convert_resources(data["paid"])
        self.status: GrantStatus = GrantStatus(data["status"])
        self.code: str = data["code"]

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
        alliance: Alliance,
        payoff: GrantPayoff,
        note: Optional[str],
        deadline: Optional[datetime.datetime],
        paid: Resources,
        status: GrantStatus,
    ) -> Grant:
        grant = cls(
            {
                "id": 0,
                "recipient": recipient.id,
                "time": str(time),
                "resources": str(resources),
                "alliance": alliance.id,
                "payoff": payoff.value,
                "note": note,
                "deadline": str(deadline) if deadline is not None else None,
                "paid": str(paid),
                "status": status.value,
                "code": funcs.utils.generate_code(),
            }
        )
        await grant.save()
        return grant

    async def save(self) -> None:
        if self.id:
            await execute_query(
                "UPDATE grants SET recipient = $2, time = $3, resources = $4, alliance = $5, payoff = $6, note = $7, deadline = $8, paid = $9, status = $10, code = $11 WHERE id = $1;",
                self.id,
                self.recipient_id,
                str(self.time),
                str(self.resources),
                self.alliance_id,
                self.payoff.value,
                self.note,
                str(self.deadline) if self.deadline is not None else None,
                str(self.paid),
                self.status.value,
                self.code,
            )
        else:
            id = await execute_read_query(
                "INSERT INTO grants (recipient, time, resources, alliance, payoff, note, deadline, paid, status, code) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING id;",
                self.recipient_id,
                str(self.time),
                str(self.resources),
                self.alliance_id,
                self.payoff.value,
                self.note,
                str(self.deadline) if self.deadline is not None else None,
                str(self.paid),
                self.status.value,
                self.code,
            )
            self.id = id[0]["id"]
            cache.add_grant(self)

    async def send(
        self, creator: Union[discord.Member, discord.User], request: bool = True
    ) -> None:
        transaction = await Transaction.create(
            self.time,
            TransactionStatus.PENDING,
            TransactionType.GRANT if request else TransactionType.GRANT_WITHDRAW,
            creator,
            self.recipient,  # type: ignore
            self,
            self.resources,
            self.note,
            to_type=AccountType.USER,
            from_type=AccountType.GRANT,
        )
        await transaction.send_for_approval()

    @property
    def alliance(self) -> Optional[Alliance]:
        return cache.get_alliance(self.alliance_id)

    def regenerate_code(self) -> None:
        self.code = funcs.utils.generate_code(20)
