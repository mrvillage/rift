from __future__ import annotations

from typing import TYPE_CHECKING

from asyncpg import exceptions
import discord
from discord.ext.commands import (
    Context,
    MemberConverter,
    MemberNotFound,
    UserConverter,
    UserNotFound,
)

from ..data import get
from ..data.classes import Alliance, Nation
from ..errors import AllianceNotFoundError, LinkError
from ..funcs.utils import convert_link
from .link import get_link_user


async def search_alliance(ctx: Context, search: str) -> Alliance:
    try:
        search = await convert_link(search)
    except LinkError:
        pass
    user = None
    try:
        user = await MemberConverter().convert(ctx, search)
    except MemberNotFound:
        try:
            user = await UserConverter().convert(ctx, search)
        except UserNotFound:
            pass
    if user is not None:
        if TYPE_CHECKING:
            assert isinstance(user, (discord.User, discord.Member))
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
        except exceptions.DataError:
            raise AllianceNotFoundError(search)
    alliance = await get.get_alliance(search)
    if alliance is not None:
        return await Alliance.fetch(alliance.id)
    nation = await get.get_nation(search)
    if nation is not None and nation.alliance_id != 0:
        return await Alliance.fetch(nation.alliance_id)
    raise AllianceNotFoundError(search)
