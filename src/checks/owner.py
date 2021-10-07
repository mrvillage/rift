from __future__ import annotations

from discord.ext.commands import check

from ..ref import RiftContext

__all__ = ("is_owner",)


def is_owner():
    async def predicate(ctx: RiftContext):
        return await ctx.bot.is_owner(ctx.author)  # type: ignore

    return check(predicate)  # type: ignore
