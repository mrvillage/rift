from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Union

import discord
from discord.ext import commands

from .. import funcs

if TYPE_CHECKING:
    from ..data.classes import Nation


async def search_nation_author(
    ctx: commands.Context, search: str
) -> Tuple[Union[discord.User, discord.Member, discord.Guild], Nation]:
    search = str(ctx.author.id) if search is None else search
    nation = await funcs.search_nation(ctx, search)
    if nation.user is None:
        return ctx.author if ctx.guild is None else ctx.guild, nation
    else:
        return nation.user, nation


async def search_nation(ctx: commands.Context, search: str) -> Nation:
    search = str(ctx.author.id) if search is None else search
    return await funcs.search_nation(ctx, search)
