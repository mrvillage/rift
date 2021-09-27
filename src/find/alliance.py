from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from .. import funcs

__all__ = ("search_alliance",)

if TYPE_CHECKING:
    from ..data.classes import Alliance


async def search_alliance(
    ctx: commands.Context, search: str, advanced: bool = True
) -> Alliance:
    search = search or str(ctx.author.id)
    return await funcs.search_alliance(ctx, search, advanced)
