from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    import discord

def has_manage_permissions():
    async def predicate(ctx: commands.Context):
        if TYPE_CHECKING:
            assert isinstance(ctx.author, discord.Member)
            assert isinstance(ctx.guild, discord.Guild)
        perms = ctx.author.guild_permissions
        if ctx.bot.enable_debug and await ctx.bot.is_owner(ctx.author):
            return True
        if (
            perms.manage_guild
            or perms.administrator
            or ctx.guild.owner_id == ctx.author.id
        ):
            return True
        raise commands.MissingPermissions(["manage"])

    return commands.check(predicate)
