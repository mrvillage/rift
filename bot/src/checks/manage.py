from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from ..data.classes import GuildSettings, Nation
from ..ref import RiftContext

__all__ = (
    "can_manage_alliance_roles",
    "has_alliance_manage_permissions",
    "has_manage_permissions",
)

if TYPE_CHECKING:
    from typing import Optional

    import discord

    from ..data.classes import Alliance


async def can_manage_alliance_roles(
    nation: Nation, alliance: Optional[Alliance], suppress: bool = False
):
    if alliance is None:
        return False
    if nation.alliance_position >= 4 and nation.alliance_id == alliance.id:
        return True
    user = nation.user
    if user is None:
        return False
    permissions = alliance.permissions_for(user)
    if permissions.leadership or permissions.manage_roles:
        return True
    if suppress:
        return False
    raise commands.MissingPermissions(["alliance_manage_roles"])


def has_alliance_manage_permissions():
    async def predicate(ctx: RiftContext):
        nation = await Nation.convert(ctx, None)
        if nation.alliance_position >= 3:
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
