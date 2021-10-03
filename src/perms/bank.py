from __future__ import annotations

from typing import Any, Dict, List, Union

from discord import Member, User

from ..data.classes import Nation
from ..data.db import execute_read_query
from ..funcs.utils import get_alliance_position_id

__all__ = ("check_bank_perms",)


async def check_bank_perms(*, nation: Nation, author: Union[Member, User], action: str):
    """ACTION MUST BE 'send' or 'view'"""
    try:
        perm: Dict[str, Any] = (
            await execute_read_query(
                "SELECT * FROM bankpermissions WHERE allianceid = 3683;"
            )
        )[0]
        nation_position = get_alliance_position_id(nation.alliance_position)
        alliance_position = get_alliance_position_id(perm[f"{action}rank"])
        await nation.make_attrs("alliance")
        if nation.alliance is None:
            return False
        if nation_position >= alliance_position and nation.alliance.id == 3683:
            return True
        if (
            author.id in perm[f"{action}users"]
            if perm[f"{action}users"] is not None
            else []
        ):
            return True
        if isinstance(author, User):
            return False
        roles = [role.id for role in author.roles]
        role_perms: List[int] = (
            perm[f"{action}roles"] if perm[f"{action}roles"] is not None else []
        )
        return any(role in role_perms for role in roles)
    except Exception:
        return False
