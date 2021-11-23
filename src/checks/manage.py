from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from ..cache import cache
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


async def can_manage_alliance_roles(nation: Nation, alliance: Optional[Alliance]):
    if alliance is None:
        return False
    if nation.alliance_position in {"Officer", "Heir", "Leader"}:
        return True
    roles = [i for i in cache.roles if i.alliance_id == alliance.id]
    if any(
        role.permissions.manage_roles or role.permissions.leadership
        for role in roles
        if nation.id in role.member_ids
    ):
        return True
    raise commands.MissingPermissions(["alliance_manage_roles"])


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
