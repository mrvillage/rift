from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List, Literal, Optional

import discord
from discord.ext import commands

from src.views.settings import AlliancePurposeConfirm

from ... import funcs
from ...checks import has_manage_permissions
from ...data import get
from ...data.classes import Alliance, GuildSettings, Nation
from ...errors import AllianceNotFoundError
from ...ref import Rift, RiftContext


class Settings(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="user-settings",
        aliases=["us", "usersettings", "my-settings", "mysettings"],
        invoke_without_command=True,
        enabled=False,
    )
    async def user_settings(self, ctx: RiftContext):
        ...

    @commands.group(
        name="server-settings",
        aliases=["ss", "serversettings", "settings"],
        brief="View of modify server settings.",
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings(self, ctx: RiftContext):
        ...

    @server_settings.command(  # type: ignore
        name="purpose",
        aliases=["p"],
        brief="View or modify the server's purpose.",
        type=commands.CommandType.chat_input,
        descriptions={"purpose": "The new purpose of the server."},
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_purpose(
        self,
        ctx: RiftContext,
        *,
        purpose: Optional[
            Literal[  # type: ignore
                "ALLIANCE",
                "ALLIANCE_GOVERNMENT",
                "ALLIANCE_MILITARY_AFFAIRS",
                "ALLIANCE_INTERNAL_AFFAIRS",
                "ALLIANCE_MILITARY_AFFAIRS",
                "ALLIANCE_FOREIGN_AFFAIRS",
                "ALLIANCE_ECONOMIC_AFFAIRS",
                "BUSINESS",
                "COMMUNITY",
                "PERSONAL",
            ]
        ] = None,
    ):  # sourcery no-metrics
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id)
        if purpose is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The current server purpose is `{settings.purpose}`.",
                    color=discord.Color.blue(),
                )
            )
        if purpose.lower() == "none":
            purpose = None
        if not purpose:
            await settings.set_(purpose=purpose, purpose_argument=None)
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="The server has been set to have no purpose.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        if purpose == "PERSONAL":
            if settings.purpose == "PERSONAL":
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="The server purpose is already set to `PERSONAL`!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            await settings.set_(purpose=purpose, purpose_argument=None)
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The server purpose has been set to: `{purpose}`",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        elif purpose.startswith("ALLIANCE"):
            message = await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Waiting for a followup message with the alliance...",
                    color=discord.Color.orange(),
                ),
                return_message=True,
            )
            try:
                m = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                    timeout=60,
                )
            except asyncio.TimeoutError:
                return await message.edit(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="You didn't provide an alliance in time!",
                        color=discord.Color.red(),
                    )
                )
            try:
                alliance = await Alliance.convert(ctx, m.content)
            except AllianceNotFoundError:
                return await message.edit(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"No alliance found with argument `{message.content}`",
                        color=discord.Color.red(),
                    )
                )
            if settings.purpose == purpose and settings.purpose_argument == str(
                alliance.id
            ):
                return await message.edit(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The server purpose is already set to `{purpose}` and is linked to {repr(alliance)}!",
                        color=discord.Color.green(),
                    )
                )
            for i in alliance.leaders:
                await i.make_attrs("user")
            if all(not i.user for i in alliance.leaders):
                return await message.edit(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"{repr(alliance)} has no linked leaders! Have at least one link themselves to provide confirmation then try again.",
                        color=discord.Color.red(),
                    )
                )
            await message.edit(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"Sending messages to the leaders of {repr(alliance)}...",
                    color=discord.Color.orange(),
                )
            )
            sent: List[discord.User] = []
            for i in alliance.leaders:
                if not i.user:
                    continue
                view = AlliancePurposeConfirm(purpose, alliance, i.user, settings)
                try:
                    await view.start()
                    sent.append(i.user)
                except discord.Forbidden:
                    continue
            if sent:
                await message.edit(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"Waiting for confirmation from a linked alliance leader before setting the purpose to `{purpose}` and link to {repr(alliance)}.",
                        color=discord.Color.green(),
                    )
                )
            else:
                await message.edit(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="I couldn't send a message to any alliance leaders!.",
                        color=discord.Color.red(),
                    )
                )
        else:
            message = await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Waiting for a followup message with the community or business name...",
                    color=discord.Color.orange(),
                ),
                ephemeral=True,
                return_message=True,
            )
            try:
                m = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                    timeout=60,
                )
            except asyncio.TimeoutError:
                return await message.edit(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="You didn't provide a name in time!",
                        color=discord.Color.red(),
                    )
                )
            if settings.purpose == purpose and settings.purpose_argument == m.content:
                return await message.edit(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The server purpose is already set to `{purpose}` with the name `{m.content}`!",
                        color=discord.Color.red(),
                    )
                )
            await settings.set_(purpose=purpose, purpose_argument=m.content)
            await message.edit(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The server purpose has been set to `{purpose}` with the name `{m.content}`.",
                    color=discord.Color.green(),
                )
            )

    @server_settings.command(  # type: ignore
        name="welcome-message",
        aliases=["wm", "welcomemessage"],
        brief="Modify the server's welcome message.",
        type=commands.CommandType.chat_input,
        descriptions={
            "message": "The new welcome message.",
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_welcome_message(
        self, ctx: RiftContext, *, message: str = None  # type: ignore
    ):
        message: Optional[str]
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if message is None:
            return await ctx.send(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The current welcome message is `{settings.welcome_settings.welcome_message}`.",
                    color=discord.Color.blue(),
                )
            )
        if message:
            message = message.strip("\n ")
        if message.lower() == "none":
            message = None
        await settings.welcome_settings.set_(welcome_message=message)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description=f"The welcome message has been set to:\n\n{message}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @server_settings.command(  # type: ignore
        name="verified-nickname",
        aliases=["vn", "verifiednickname"],
        brief="Modify the server's verified nickname format.",
        type=commands.CommandType.chat_input,
        descriptions={
            "nickname": "The new verified nickname format.",
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_verified_nickname(
        self, ctx: RiftContext, *, nickname: str = None  # type: ignore
    ):
        nickname: Optional[str]
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if nickname is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The verified nickname format is set to:\n\n`{settings.welcome_settings.verified_nickname}`",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        if nickname:
            nickname = nickname.strip("\n ")
        if nickname.lower() == "none":
            nickname = None
        await settings.welcome_settings.set_(verified_nickname=nickname)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description=f"The verified nickname format has been set to:\n\n`{nickname}`",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @server_settings.command(  # type: ignore
        name="welcome-channels",
        brief="Modify the server's welcome channels format.",
        type=commands.CommandType.chat_input,
        descriptions={
            "channels": "The new welcome channels, given by space separated channel mentions.",
            "clear": "Set to True to clear the welcome channels.",
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_welcome_channels(
        self, ctx: RiftContext, *, channels: List[discord.TextChannel] = None, clear: bool = False  # type: ignore
    ):
        channels: Optional[str]
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if TYPE_CHECKING:
            assert settings.welcome_settings is not None
        if channels is None and not clear:
            if settings.welcome_settings.welcome_channels:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The welcome channels are:\n\n{''.join(f'<#{i}>' for i in settings.welcome_settings.welcome_channels)}",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
            else:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="This server has no welcome channels.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        channels_set = None if clear else [i.id for i in channels]  # type: ignore
        await settings.welcome_settings.set_(welcome_channels=channels_set)
        if channels_set:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The welcome channels are now:\n\n{''.join(f'<#{i}>' for i in channels_set)}",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="The welcome channels have been cleared.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

    @server_settings.command(  # type: ignore
        name="join-roles",
        brief="Modify the server's join roles.",
        type=commands.CommandType.chat_input,
        descriptions={
            "roles": "The new join roles, given by space separated role mentions.",
            "clear": "Set to True to clear the join roles.",
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_join_roles(
        self, ctx: RiftContext, *, roles: List[discord.Role] = None, clear: bool = False  # type: ignore
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if TYPE_CHECKING:
            assert settings.welcome_settings is not None
        if roles is None and not clear:
            if settings.welcome_settings.join_roles:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The join roles are:\n\n{''.join(f'<@&{i}>' for i in settings.welcome_settings.join_roles)}",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
            else:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="This server has no join roles.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        roles_set = None if clear else [i.id for i in roles]  # type: ignore
        await settings.welcome_settings.set_(join_roles=roles_set)
        if roles_set:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The join roles are now:\n\n{''.join(f'<@&{i}>' for i in roles_set)}",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="The join roles have been cleared.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

    @server_settings.command(  # type: ignore
        name="managers",
        brief="Modify the server's manager roles.",
        type=commands.CommandType.chat_input,
        descriptions={
            "roles": "The new manager roles, given by space separated role mentions.",
            "clear": "Set to True to clear the manager roles.",
        },
    )
    @has_manage_permissions(managers=False)
    @commands.guild_only()
    async def server_settings_managers(
        self, ctx: RiftContext, *, roles: List[discord.Role] = None, clear: bool = False  # type: ignore
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id)
        if roles is None and not clear:
            if settings.manager_role_ids:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The join roles are:\n\n{''.join(f'<@&{i}>' for i in settings.manager_role_ids)}",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
            else:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="This server has no manager roles.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        roles_set = None if clear else [i.id for i in roles]  # type: ignore
        await settings.set_(manager_role_ids=roles_set)
        if roles_set:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The manager roles are now:\n\n{''.join(f'<@&{i}>' for i in roles_set)}",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="The manager roles have been cleared.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # sourcery no-metrics skip: merge-nested-ifs
        if member.pending:
            return
        try:
            nat = await get.get_link_user(member.id)
            nation: Optional[Nation] = await Nation.fetch(nat["nation_id"])
            await nation.make_attrs("alliance")
        except IndexError:
            nation = None
        settings = await GuildSettings.fetch(member.guild.id, "welcome_settings")
        settings = settings.welcome_settings
        if settings.welcome_channels:
            for channel in settings.welcome_channels:
                channel = self.bot.get_channel(channel)
                if not channel:
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
