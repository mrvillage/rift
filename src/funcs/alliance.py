from src.data.classes.alliance import Alliance
from src.data.classes.nation import Nation
from discord.ext.commands import (
    Context,
    MemberConverter,
    MemberNotFound,
    UserConverter,
    UserNotFound,
)

from ..data import get
from ..errors import AllianceNotFoundError, LinkError
from ..funcs.utils import convert_link
from .link import get_link_user


async def search_alliance(ctx: Context, search):
    try:
        search = await convert_link(search)
    except LinkError:
        pass
    try:
        user = await MemberConverter().convert(ctx, search)
    except MemberNotFound:
        try:
            user = await UserConverter().convert(ctx, search)
        except UserNotFound:
            pass
    if "user" in locals():
        try:
            return await Alliance.fetch(
                (await Nation.fetch((await get_link_user(user.id))[1])).alliance_id
            )
        except IndexError:
            pass
    if search.isdigit():
        try:
            return await Alliance.fetch(int(search))
        except KeyError:
            pass
    alliance = await get.get_alliance(search)
    if alliance is not None:
        return await Alliance.fetch(alliance.id)
    nation = await get.get_nation(search)
    if nation is not None:
        if nation.alliance_id != 0:
            return await Alliance.fetch(nation.alliance_id)
    raise AllianceNotFoundError
