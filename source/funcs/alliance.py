from discord.ext.commands import Context, MemberConverter, UserConverter, MemberNotFound, UserNotFound
from .link import get_link_user, get_link_nation
from .. import cache
from ..errors import AllianceNotFoundError, LinkError
from ..data import get
from ..funcs.utils import convert_link


async def search_alliance(ctx: Context, search):
    try:
        search = convert_link(search)
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
        return cache.nations[(await get_link_user(user.id))[1]].alliance
    if search.isdigit():
        try:
            return cache.alliances[int(search)]
        except KeyError:
            pass
    alliance = await get.get_alliance(search)
    if alliance is not None:
        return cache.alliances[alliance.id]
    nation = await get.get_nation(search)
    if nation is not None:
        if nation.alliance_id != 0:
            return cache.alliances[nation.alliance_id]
    raise AllianceNotFoundError
