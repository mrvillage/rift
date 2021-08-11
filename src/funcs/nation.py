from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from asyncpg import exceptions
from discord.ext.commands import (
    Context,
    MemberConverter,
    MemberNotFound,
    UserConverter,
    UserNotFound,
)

from ..data import get
from ..data.classes import Nation
from ..errors import LinkError, NationNotFoundError
from ..funcs.utils import convert_link
from .link import get_link_user


async def search_nation(ctx: Context, search: str) -> Nation:
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
            return await Nation.fetch((await get_link_user(user.id))[1])
        except IndexError:
            pass
    if search.isdigit():
        try:
            return await Nation.fetch(int(search))
        except KeyError:
            pass
        except exceptions.DataError:
            raise NationNotFoundError(search)
    nation = await get.get_nation(search)
    if nation is not None:
        return nation
    raise NationNotFoundError(search)
