import json
from typing import Union
from discord import Member, User
from ..data.db import execute_read_query
from ..data.classes import Nation
from ..funcs.utils import get_alliance_position_id


async def check_bank_perms(*, nation: Nation, author: Union[Member, User], action):
    """ACTION MUST BE 'send' or 'view'"""
    try:
        perm = (await execute_read_query("SELECT * FROM bankpermissions WHERE allianceid = $1;", nation.alliance.id))[0]
        nation_position = get_alliance_position_id(nation.alliance_position)
        alliance_position = get_alliance_position_id(perm[f"{action}rank"])
        if nation_position >= alliance_position:
            return True
        if author.id in json.loads(perm[f'{action}users']) if perm[f'{action}users'] is not None else []:
            return True
        roles = [role.id for role in author.roles]
        role_perms = json.loads(perm[f'{action}roles']) if perm[f'{action}roles'] is not None else []
        if any(role in role_perms for role in roles):
            return True
        return False
    except Exception:  # pylint: disable=broad-except
        return False
