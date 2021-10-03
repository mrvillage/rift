from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, Union

import discord

from .. import funcs
from ..ref import RiftContext

if TYPE_CHECKING:
    from ..data.classes import Nation


async def search_nation_author(
    ctx: RiftContext, search: str
) -> Tuple[Union[discord.User, discord.Member, discord.Guild], Nation]:
    search = str(ctx.author.id) if search is None else search
    nation = await funcs.search_nation(ctx, search)
    if nation.user is None:
        return ctx.author if ctx.guild is None else ctx.guild, nation
    else:
        return nation.user, nation


async def search_nation(
    ctx: RiftContext, search: Optional[str], advanced: bool = True
) -> Nation:
    search = search or str(ctx.author.id)
    return await funcs.search_nation(ctx, search, advanced)
