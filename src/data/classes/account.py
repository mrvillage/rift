from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from ... import funcs
from ...cache import cache
from ...errors import AccountNotFoundError
from ...ref import RiftContext, bot
from ..db import execute_query, execute_read_query
from .resources import Resources

__all__ = ("Account",)

if TYPE_CHECKING:
    from typing import Optional, Union

    from _typings import AccountData

    from .alliance import Alliance


class Account:
    __slots__ = (
        "id",
        "name",
        "owner_id",
        "alliance_id",
        "resources",
        "war_chest",
        "primary",
        "deposit_code",
    )

    def __init__(self, data: AccountData):
        self.id: int = data.get("id", 0)
        self.name: str = data["name"]
        self.owner_id: int = data["owner"]
        self.alliance_id: int = data["alliance"]
        self.resources: Resources = Resources.convert_resources(data["resources"])
        self.war_chest: bool = data["war_chest"]
        self.primary: bool = data["primary_"]
        self.deposit_code: Optional[str] = data["deposit_code"]

    async def save(self) -> None:
        if self.id:
            await execute_query(
                "UPDATE accounts SET name = $2, owner = $3, alliance = $4, resources = $5, war_chest = $6, primary_ = $7, deposit_code = $8 WHERE id = $1;",
                self.id,
                self.name,
                self.owner_id,
                self.alliance_id,
                str(self.resources),
                self.war_chest,
                self.primary,
                self.deposit_code,
            )
        else:
            id = await execute_read_query(
                "INSERT INTO accounts (name, owner, alliance, resources, war_chest, primary_, deposit_code) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id;",
                self.name,
                self.owner_id,
                self.alliance_id,
                str(self.resources),
                self.war_chest,
                self.primary,
                self.deposit_code,
            )
            self.id = id[0]["id"]
            cache.add_account(self)

    async def delete(self) -> None:
        await execute_query("DELETE FROM accounts WHERE id = $1;", self.id)
        cache.remove_account(self)

    @classmethod
    async def create(
        cls,
        owner: Union[discord.Member, discord.User],
        alliance: Alliance,
        name: str,
        war_chest: bool,
        primary: bool,
    ) -> Account:
        account = cls(
            {
                "id": 0,
                "name": name,
                "owner": owner.id,
                "alliance": alliance.id,
                "resources": "",
                "war_chest": war_chest,
                "primary_": primary,
                "deposit_code": funcs.utils.generate_code(20),
            }
        )
        await account.save()
        cache.add_account(account)
        return account

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str) -> Account:
        try:
            i = funcs.utils.convert_int(argument)
        except ValueError:
            pass
        else:
            account = cache.get_account(i)
            if account:
                return account
        accounts = [i for i in cache.accounts if i.name.lower() == argument.lower()]
        if len(accounts) == 1:
            return accounts[0]
        raise AccountNotFoundError(argument)

    @property
    def owner(self) -> Optional[discord.User]:
        return bot.get_user(self.owner_id)

    @property
    def alliance(self) -> Optional[Alliance]:
        return cache.get_alliance(self.alliance_id)

    def regenerate_deposit_code(self) -> None:
        self.deposit_code = funcs.utils.generate_code(20)
