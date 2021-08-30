from __future__ import annotations
from ...checks import has_manage_permissions

from typing import TYPE_CHECKING, Optional

import discord
from discord import NotFound
from discord.ext import commands

from ... import funcs
from ...data.classes import GuildSettings
from ...data.classes import Nation


if TYPE_CHECKING:
    from ...ref import Rift


class Settings(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="user-settings",
        aliases=["us", "usersettings", "my-settings", "mysettings"],
        invoke_without_command=True,
        enabled=False,
    )
    async def user_settings(self, ctx: commands.Context):
        ...

    @commands.group(
        name="server-settings",
        aliases=["ss", "serversettings", "settings"],
        help="View of modify server settings.",
        invoke_without_command=True,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings(self, ctx: commands.Context):
        ...

    @server_settings.command(
        name="purpose",
        aliases=["p"],
        help="View or modify the server's purpose.",
        enabled=False,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_purpose(self, ctx: commands.Context):
        ...

    @server_settings.command(
        name="welcome-message",
        aliases=["wm", "welcomemessage"],
        help="Modify the server's welcome message.",
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_welcome_message(
        self, ctx: commands.Context, *, message: str = None
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if message:
            message = message.strip("\n ")
        await settings.welcome_settings.set_(welcome_message=message)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description=f"The welcome message has been set to:\n\n{message}",
            )
        )

    @server_settings.command(
        name="verified-nickname",
        aliases=["vn", "verifiednickname"],
        help="Modify the server's verified nickname format.",
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_verified_nickname(
        self, ctx: commands.Context, *, nickname: str = None
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if nickname:
            nickname = nickname.strip("\n ")
        await settings.welcome_settings.set_(verified_nickname=nickname)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description=f"The verified nickname format has been set to:\n\n`{nickname}`",
            )
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # sourcery no-metrics skip: merge-nested-ifs
        if member.pending:
            return
        try:
            nat = await funcs.get_link_user(member.id)
            nation: Optional[Nation] = await Nation.fetch(nat["nation_id"])
            await nation.make_attrs("alliance")
        except IndexError:
            nation = None
        settings = await GuildSettings.fetch(member.guild.id, "welcome_settings")
        settings = settings.welcome_settings
        if settings.welcome_channels:
            for channel in settings.welcome_channels:
                try:
                    channel = await self.bot.fetch_channel(channel)
                except NotFound:
                    continue
                try:
                    embed = settings.format_welcome_embed(member, bool(nation))
                    await channel.send(embed=embed)  # type: ignore
                except discord.Forbidden:
                    try:
                        await channel.send(  # type: ignore
                            f"Something went wrong welcoming {member.mention} to the server!"
                        )
                    except discord.Forbidden:
                        continue
        roles: list[discord.Role] = []
        highest_role: discord.Role = member.guild.get_member(self.bot.user.id).top_role  # type: ignore
        if settings.join_roles is not None:
            for role_id in settings.join_roles:
                role: Optional[discord.Role] = member.guild.get_role(role_id)
                if role is None:
                    continue
                if highest_role > role:
                    roles.append(role)
            if roles:
                await member.add_roles(*roles)
            roles = []
        if nation:
            if settings.verified_nickname:
                if member.guild.get_member(
                    self.bot.user.id  # type: ignore
                ).guild_permissions.manage_nicknames:  # type: ignore
                    await settings.set_verified_nickname(member, nation)
            if settings.verified_roles is not None:
                for role_id in settings.verified_roles:
                    role: Optional[discord.Role] = member.guild.get_role(role_id)
                    if role is None:
                        continue
                    if highest_role > role:
                        roles.append(role)
                if roles:
                    await member.add_roles(*roles)
                roles = []
            ...  # implement the rest of the welcome stuff below, will need to set up alliance settings and embassies first though

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.pending and not after.pending:
            await self.on_member_join(after)


def setup(bot: Rift):
    bot.add_cog(Settings(bot))
