from discord.ext.commands import Context, MemberConverter, UserConverter, MemberNotFound, UserNotFound
from .link import get_link_user, get_link_nation
from .. import cache
from ..errors import NationNotFoundError, LinkError
from ..data import get
from ..funcs.utils import convert_link


async def search_nation(ctx: Context, search):
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
        return cache.nations[(await get_link_user(user.id))[1]]
    if search.isdigit():
        try:
            return cache.nations[int(search)]
        except KeyError:
            pass
    nation = await get.get_nation(search)
    if nation is not None:
        return nation
    nation = await get.get_nation(search)
    raise NationNotFoundError
