from __future__ import annotations

from typing import TYPE_CHECKING

from discord.abc import Snowflake

from ...cache import cache
from ...data.db import execute_query, execute_read_query
from ...flags import RolePermissions

__all__ = ("Role",)

if TYPE_CHECKING:
    from typing import List, Optional

    from _typings import RoleData

    from .alliance import Alliance
    from .nation import Nation


class Role:
    __slots__ = (
        "id",
        "name",
        "description",
        "alliance_id",
        "rank",
        "permissions",
        "member_ids",
    )

    def __init__(self, data: RoleData) -> None:
        self.id: int = data.get("id", 0)
        self.name: str = data["name"]
        self.description: Optional[str] = data["description"]
        self.alliance_id: int = data["alliance"]
        self.rank: int = data["rank"]
        self.permissions: RolePermissions = RolePermissions(data["permissions"])
        self.member_ids: List[int] = data["members"]

    @property
    def alliance(self) -> Optional[Alliance]:
        return cache.get_alliance(self.alliance_id)

    async def save(self) -> None:
        if self.id:
            await execute_query(
                "UPDATE roles SET name = $2, description = $3, alliance = $4, rank = $5, permissions = $6, members = $7 WHERE id = $1;",
                self.id,
                self.name,
                self.description,
                self.alliance_id,
                self.rank,
                self.permissions.flags,
                self.member_ids,
            )
        else:
            id = await execute_read_query(
                "INSERT INTO roles (name, description, alliance, rank, permissions, members) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id;",
                self.name,
                self.description,
                self.alliance_id,
                self.rank,
                self.permissions.flags,
                self.member_ids,
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
            }
        )
