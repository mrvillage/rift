from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.abc import Snowflake

from ...cache import cache
from ...data.db import execute_query, execute_read_query
from ...enums import PrivacyLevel
from ...errors import RoleNotFoundError
from ...flags import RolePermissions
from ...ref import bot
from .nation import Nation

__all__ = ("Role",)

if TYPE_CHECKING:
    from typing import List, Optional

    from _typings import RoleData

    from ...ref import RiftContext
    from .alliance import Alliance


class Role:
    __slots__ = (
        "id",
        "name",
        "description",
        "alliance_id",
        "rank",
        "permissions",
        "member_ids",
        "privacy_level",
    )

    def __init__(self, data: RoleData) -> None:
        self.id: int = data.get("id", 0)
        self.name: str = data["name"]
        self.description: Optional[str] = data["description"]
        self.alliance_id: int = data["alliance"]
        self.rank: int = data["rank"]
        self.permissions: RolePermissions = RolePermissions(data["permissions"])
        self.member_ids: List[int] = data["members"]
        self.privacy_level: PrivacyLevel = PrivacyLevel(data["privacy_level"])

    @classmethod
    async def convert(cls, ctx: RiftContext, argument: str) -> Role:
        from ...funcs.utils import convert_int

        try:
            role = cache.get_role(convert_int(argument))
            if role:
                return role
        except ValueError:
            pass
        try:
            nation = await Nation.convert(ctx, None)
            roles = [i for i in cache.roles if i.alliance_id == nation.alliance_id]
            roles = [i for i in roles if i.name.lower() == argument.lower()]
            if len(roles) == 1:
                return roles[0]
        except StopIteration:
            pass
        raise RoleNotFoundError(argument)

    @property
    def alliance(self) -> Optional[Alliance]:
        return cache.get_alliance(self.alliance_id)

    @property
    def members(self) -> List[discord.User]:
        return [u for i in self.member_ids if (u := bot.get_user(i)) is not None]

    async def save(self) -> None:
        if self.id:
            await execute_query(
                "UPDATE roles SET name = $2, description = $3, alliance = $4, rank = $5, permissions = $6, members = $7, privacy_level = $8 WHERE id = $1;",
                self.id,
                self.name,
                self.description,
                self.alliance_id,
                self.rank,
                self.permissions.flags,
                self.member_ids,
                self.privacy_level.value,
            )
        else:
            id = await execute_read_query(
                "INSERT INTO roles (name, description, alliance, rank, permissions, members, privacy_level) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id;",
                self.name,
                self.description,
                self.alliance_id,
                self.rank,
                self.permissions.flags,
                self.member_ids,
                self.privacy_level.value,
            )
            self.id = id[0]["id"]
            cache.add_role(self)

    def add_members(self, *args: Nation) -> None:
        for arg in args:
            if arg.id not in self.member_ids:
                self.member_ids.append(arg.id)

    def remove_members(self, *args: Nation) -> None:
        for arg in args:
            if arg.id in self.member_ids:
                self.member_ids.remove(arg.id)

    @classmethod
    def create(
        cls,
        name: str,
        description: Optional[str],
        alliance: Alliance,
        rank: int,
        starting_members: List[Snowflake],
        privacy: PrivacyLevel,
    ) -> Role:
        return cls(
            {
                "id": 0,
                "name": name,
                "description": description,
                "alliance": alliance.id,
                "rank": rank,
                "members": [i.id for i in starting_members],
                "permissions": 0,
                "privacy_level": privacy.value,
            }
        )

    async def delete(self) -> None:
        await execute_query("DELETE FROM roles WHERE id = $1;", self.id)
        cache.remove_role(self)
