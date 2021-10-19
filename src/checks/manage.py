from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from ..data.classes import GuildSettings, Nation
from ..ref import RiftContext

__all__ = ("has_alliance_manage_permissions", "has_manage_permissions")

if TYPE_CHECKING:
    import discord


def has_alliance_manage_permissions():
    async def predicate(ctx: RiftContext):
        nation = await Nation.convert(ctx, None)
        if nation.alliance_position in {"Officer", "Heir", "Leader"}:
            return True
        raise commands.MissingPermissions(["alliance_manage"])

    return commands.check(predicate)  # type: ignore


def has_manage_permissions(managers: bool = True):
    async def predicate(ctx: RiftContext):
        if TYPE_CHECKING:
            assert isinstance(ctx.author, discord.Member)
            assert isinstance(ctx.guild, discord.Guild)
        perms = ctx.author.guild_permissions
        settings = await GuildSettings.fetch(ctx.guild.id)
        if (
            ctx.bot.enable_debug
            and await ctx.bot.is_owner(ctx.author)  # type: ignore
            or (
                managers
                and any(
                    i.id in (settings.manager_role_ids or []) for i in ctx.author.roles
                )
            )
        ):
            return True
        if (
            perms.manage_guild
            or perms.administrator
            or ctx.guild.owner_id == ctx.author.id
        ):
            return True
        if managers:
            raise commands.MissingPermissions(["manage_no_role"])
        raise commands.MissingPermissions(["manage"])

    return commands.check(predicate)  # type: ignore
