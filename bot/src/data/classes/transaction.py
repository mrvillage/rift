from __future__ import annotations

import datetime
import time
from typing import TYPE_CHECKING

import discord

from ... import funcs
from ...cache import cache
from ...enums import AccountType, TransactionStatus, TransactionType
from ...errors import TransactionNotFoundError
from ...ref import RiftContext, bot
from ..db import execute_query, execute_read_query
from .resources import Resources
from .settings import AllianceSettings

__all__ = ("Transaction", "TransactionRequest")

if TYPE_CHECKING:
    from typing import Optional, Union

    from _typings import Field, TransactionData, TransactionRequestData

    from ...views import TransactionRequestView
    from .account import Account
    from .alliance import Alliance
    from .grant import Grant
    from .nation import Nation


class Transaction:
    __slots__ = (
        "id",
        "time",
        "status",
        "type",
        "status",
        "creator_id",
        "to_id",
        "from_id",
        "resources",
        "note",
        "to_type",
        "from_type",
    )

    def __init__(self, data: TransactionData) -> None:
        self.id: int = data.get("id", 0)
        self.time: datetime.datetime = datetime.datetime.fromisoformat(data["time"])
        self.status: TransactionStatus = TransactionStatus(data["status"])
        self.type: TransactionType = TransactionType(data["type"])
        self.creator_id: int = data["creator"]
        self.to_id: int = data["to_"]
        self.from_id: int = data["from_"]
        self.resources: Resources = Resources.convert_resources(data["resources"])
        self.note: Optional[str] = data["note"]
        self.to_type: AccountType = AccountType(data["to_type"])
        self.from_type: AccountType = AccountType(data["from_type"])

    async def save(self) -> None:
        if self.id:
            await execute_query(
                "UPDATE transactions SET time = $2, status = $3, type = $4, creator = $5, to_ = $6, from_ = $7, resources = $8, note = $9, to_type = $10, from_type = $11 WHERE id = $1;",
                self.id,
                str(self.time),
                self.status.value,
                self.type.value,
                self.creator_id,
                self.to_id,
                self.from_id,
                str(self.resources),
                self.note,
                self.to_type.value,
                self.from_type.value,
            )
        else:
            id = await execute_read_query(
                "INSERT INTO transactions (time, status, type, creator, to_, from_, resources, note, to_type, from_type) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING id;",
                str(self.time),
                self.status.value,
                self.type.value,
                self.creator_id,
                self.to_id,
                self.from_id,
                str(self.resources),
                self.note,
                self.to_type.value,
                self.from_type.value,
            )
            self.id = id[0]["id"]
            cache.add_transaction(self)

    async def delete(self) -> None:
        await execute_query("DELETE FROM transaction WHERE id = $1;", self.id)
        cache.remove_transaction(self)

    @classmethod
    async def create(
        cls,
        time: datetime.datetime,
        status: TransactionStatus,
        type: TransactionType,
        creator: Union[discord.Member, discord.User],
        to: Union[Account, Alliance, Nation, discord.Member, discord.User, Grant],
        from_: Union[Account, Alliance, Nation, discord.Member, discord.User, Grant],
        resources: Resources,
        note: Optional[str] = None,
        *,
        to_type: AccountType = AccountType.ACCOUNT,
        from_type: AccountType = AccountType.ACCOUNT,
    ) -> Transaction:
        transaction = cls(
            {
                "id": 0,
                "time": str(time),
                "status": status.value,
                "type": type.value,
                "creator": creator.id,
                "to_": to.id,
                "from_": from_.id,
                "resources": str(resources),
                "note": note or None,
                "to_type": to_type.value,
                "from_type": from_type.value,
            }
        )
        await transaction.save()
        return transaction

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str) -> Transaction:
        try:
            i = funcs.utils.convert_int(argument)
        except ValueError:
            pass
        else:
            transaction = cache.get_transaction(i)
            if transaction:
                return transaction
        raise TransactionNotFoundError(argument)

    @property
    def creator(self) -> Optional[discord.User]:
        return bot.get_user(self.creator_id)

    @property
    def to(self) -> Optional[Account]:
        return cache.get_account(self.to_id)

    @property
    def to_nation(self) -> Optional[Nation]:
        return cache.get_nation(self.to_id)

    @property
    def to_alliance(self) -> Optional[Alliance]:
        return cache.get_alliance(self.to_id)

    @property
    def to_user(self) -> Optional[discord.User]:
        return bot.get_user(self.to_id)

    @property
    def to_grant(self) -> Optional[Grant]:
        return cache.get_grant(self.to_id)

    @property
    def from_(self) -> Optional[Account]:
        return cache.get_account(self.from_id)

    @property
    def from_nation(self) -> Optional[Nation]:
        return cache.get_nation(self.from_id)

    @property
    def from_alliance(self) -> Optional[Alliance]:
        return cache.get_alliance(self.from_id)

    @property
    def from_user(self) -> Optional[discord.User]:
        return bot.get_user(self.from_id)

    @property
    def from_grant(self) -> Optional[Grant]:
        return cache.get_grant(self.from_id)

    @property
    def field(self) -> Field:
        return {
            "name": f"ID: {self.id}",
            "value": f"Time: <t:{int(time.mktime(self.time.timetuple()))}:f>\n"
            f"Status: {self.status.name}\n"
            f"Type: {self.type.name}\n"
            f"To: {repr(self.to_alliance) if self.to_type is AccountType.ALLIANCE else repr(self.to_nation) if self.to_type is AccountType.NATION else f'#{self.to.id:,}' if self.to is not None else 'None'}  ({self.to_type.name})\n"
            f"From: {repr(self.from_alliance) if self.from_type is AccountType.ALLIANCE else repr(self.from_nation) if self.from_type is AccountType.NATION else f'#{self.from_.id:,}' if self.from_ is not None else 'None'} ({self.from_type.name})\n"
            f"Resources: {self.resources}\n"
            f"Note: {self.note}",
        }

    async def send_for_approval(self) -> None:
        from ...funcs import get_embed_author_member

        if self.status is not TransactionStatus.PENDING:
            return
        if self.type is TransactionType.TRANSFER:
            if self.to is None or self.creator is None:
                return
            user = self.to.owner
            if user is None:
                return
            request = await TransactionRequest.create(self, user)
            await user.send(
                embed=get_embed_author_member(
                    user,
                    f"{self.creator.mention} has sent you a transfer request of {self.resources} as transaction #{self.id}. Please accept or reject it below.",
                ),
                view=request.view,
            )
        if self.type is TransactionType.DEPOSIT:
            return
        if self.type is TransactionType.WITHDRAW:
            if self.from_ is None:
                return
            creator = self.creator
            if creator is None:
                return
            settings = await AllianceSettings.fetch(self.from_.alliance_id)
            request = await TransactionRequest.create(self, None)
            for channel in settings.withdraw_channels_:
                try:
                    await channel.send(
                        embed=get_embed_author_member(
                            creator,
                            f"{creator.mention} wants to withdraw {self.resources} from account #{self.from_.id} as transaction #{self.id}. Please accept or reject it below.",
                            color=discord.Color.orange(),
                        ),
                        view=request.view,
                    )
                except discord.Forbidden:
                    pass
        if self.type is TransactionType.GRANT:
            user = self.to_user
            if user is None:
                return
            grant = self.from_grant
            if grant is None:
                return
            request = await TransactionRequest.create(self, user)
            await user.send(
                embed=get_embed_author_member(
                    user,
                    f"Alliance {grant.alliance} has sent you a grant of {grant.resources} with a payoff method of `{grant.payoff.name}` and {'no deadline' if grant.deadline is None else f'is due <t:{int(grant.deadline.timestamp())}:R>'} and {f'a note of {grant.note}' if grant.note else 'no note'}. Please accept or reject it below.\nGrant ID: {grant.id}",
                    color=discord.Color.orange(),
                ),
                view=request.view,
            )
        if self.type is TransactionType.GRANT_WITHDRAW:
            grant = self.from_grant
            if grant is None:
                return
            creator = self.creator
            if creator is None:
                return
            settings = await AllianceSettings.fetch(grant.alliance_id)
            request = await TransactionRequest.create(self, None)
            for channel in settings.withdraw_channels_:
                try:
                    await channel.send(
                        embed=get_embed_author_member(
                            creator,
                            f"Grant {grant.id} needs {self.resources} to be sent to {self.to_nation}. Please send them below.",
                            color=discord.Color.orange(),
                        ),
                        view=request.view,
                    )
                except discord.Forbidden:
                    pass


class TransactionRequest:
    __slots__ = (
        "id",
        "transaction_id",
        "user_id",
        "accept_custom_id",
        "reject_custom_id",
        "cancel_custom_id",
    )

    def __init__(self, data: TransactionRequestData) -> None:
        self.id: int = data.get("id", 0)
        self.transaction_id: int = data["transaction"]
        self.user_id: int = data["user_"]
        self.accept_custom_id: str = data["accept_custom_id"]
        self.reject_custom_id: str = data["reject_custom_id"]
        self.cancel_custom_id: str = data["cancel_custom_id"]

    @property
    def transaction(self) -> Optional[Transaction]:
        return cache.get_transaction(self.transaction_id)

    @property
    def view(self) -> TransactionRequestView:
        from ...views import TransactionRequestView

        return TransactionRequestView(self, self.user_id)

    @classmethod
    async def create(
        cls,
        transaction: Transaction,
        user: Optional[Union[discord.Member, discord.User]],
    ) -> TransactionRequest:
        from ...funcs.utils import generate_custom_id

        request = cls(
            {
                "id": 0,
                "transaction": transaction.id,
                "user_": 0 if user is None else user.id,
                "accept_custom_id": generate_custom_id(),
                "reject_custom_id": generate_custom_id(),
                "cancel_custom_id": generate_custom_id(),
            }
        )
        await request.save()
        return request

    async def save(self) -> None:
        if self.id:
            await execute_query(
                "UPDATE transaction_requests SET transaction = $2, user_ = $3, accept_custom_id = $4, reject_custom_id = $5, cancel_custom_id = $6 WHERE id = $1;",
                self.id,
                self.transaction_id,
                self.user_id,
                self.accept_custom_id,
                self.reject_custom_id,
                self.cancel_custom_id,
            )
        else:
            id = await execute_read_query(
                "INSERT INTO transaction_requests (transaction, user_, accept_custom_id, reject_custom_id, cancel_custom_id) VALUES ($1, $2, $3, $4, $5) RETURNING id;",
                self.transaction_id,
                self.user_id,
                self.accept_custom_id,
                self.reject_custom_id,
                self.cancel_custom_id,
            )
            self.id = id[0]["id"]
            cache.add_transaction_request(self)
