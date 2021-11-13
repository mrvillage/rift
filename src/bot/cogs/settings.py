from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List, Literal, Optional

import discord
from discord.ext import commands
from discord.utils import MISSING

from src.data.classes.condition import Condition
from src.data.classes.settings import AllianceAutoRole, GuildWelcomeSettings
from src.views.settings import AlliancePurposeConfirm

from ... import funcs
from ...cache import cache
from ...checks import has_alliance_manage_permissions, has_manage_permissions
from ...data import get
from ...data.classes import Alliance, AllianceSettings, GuildSettings, Nation
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
        name="alliance-settings",
        brief="View or modify alliance settings.",
        type=commands.CommandType.chat_input,
    )
    @has_alliance_manage_permissions()
    async def alliance_settings(self, ctx: RiftContext):
        ...

    @alliance_settings.command(  # type: ignore
        name="default-raid-condition",
        brief="View or modify the alliance's default condition for raid targets.",
        type=commands.CommandType.chat_input,
    )
    @has_alliance_manage_permissions()
    async def alliance_settings_default_raid_condition(
        self,
        ctx: RiftContext,
        condition: Condition = MISSING,
        clear: bool = False,
    ):
        nation = await Nation.convert(ctx, None)
        if nation.alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "You need to be in an alliance to run this command."
                )
            )
        settings = await AllianceSettings.fetch(nation.alliance.id)
        if condition is MISSING and not clear:
            if settings.default_raid_condition is None:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"{repr(nation.alliance)} has no default raid condition.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            else:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The default raid condition for {repr(nation.alliance)}is:\n\n`{settings.default_raid_condition}`",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
        await settings.set_(
            default_raid_condition=Condition.convert_to_string(condition.condition)
            if condition
            else None
        )
        if condition:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The default raid condition for {repr(nation.alliance)} is now:\n\n`{condition}`",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="The default raid condition has been cleared.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

    @alliance_settings.command(  # type: ignore
        name="default-nuke-condition",
        brief="View or modify the alliance's default condition for nuke targets.",
        type=commands.CommandType.chat_input,
    )
    @has_alliance_manage_permissions()
    async def alliance_settings_default_nuke_condition(
        self,
        ctx: RiftContext,
        condition: Condition = MISSING,
        clear: bool = False,
    ):
        nation = await Nation.convert(ctx, None)
        if nation.alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "You need to be in an alliance to run this command."
                )
            )
        settings = await AllianceSettings.fetch(nation.alliance.id)
        if condition is MISSING and not clear:
            if settings.default_nuke_condition is None:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"{repr(nation.alliance)} has no default nuke condition.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            else:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The default nuke condition for {repr(nation.alliance)}is:\n\n`{settings.default_nuke_condition}`",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
        await settings.set_(
            default_nuke_condition=Condition.convert_to_string(condition.condition)
            if condition
            else None
        )
        if condition:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The default nuke condition for {repr(nation.alliance)} is now:\n\n`{condition}`",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="The default nuke condition has been cleared.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

    @alliance_settings.command(  # type: ignore
        name="default-military-condition",
        brief="View or modify the alliance's default condition for military targets.",
        type=commands.CommandType.chat_input,
    )
    @has_alliance_manage_permissions()
    async def alliance_settings_default_military_condition(
        self,
        ctx: RiftContext,
        condition: Condition = MISSING,
        clear: bool = False,
    ):
        nation = await Nation.convert(ctx, None)
        if nation.alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "You need to be in an alliance to run this command."
                )
            )
        settings = await AllianceSettings.fetch(nation.alliance.id)
        if condition is MISSING and not clear:
            if settings.default_military_condition is None:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"{repr(nation.alliance)} has no default military condition.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            else:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The default military condition for {repr(nation.alliance)}is:\n\n`{settings.default_military_condition}`",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
        await settings.set_(
            default_nuke_condition=Condition.convert_to_string(condition.condition)
            if condition
            else None
        )
        if condition:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The default military condition for {repr(nation.alliance)} is now:\n\n`{condition}`",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="The default military condition has been cleared.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

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
        purpose: Literal[  # type: ignore
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
        ] = MISSING,
    ):  # sourcery no-metrics
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id)
        if purpose is MISSING:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The current server purpose is `{settings.purpose}`.",
                    color=discord.Color.blue(),
                )
            )
        if purpose.lower() == "none":
            purpose = None  # type: ignore
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
        self, ctx: RiftContext, *, message: str = MISSING  # type: ignore
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if message is MISSING:
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
            message = None  # type: ignore
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
        self, ctx: RiftContext, *, nickname: str = MISSING  # type: ignore
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if nickname is MISSING:
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
            nickname = None  # type: ignore
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
        self,
        ctx: RiftContext,
        *,
        channels: List[discord.TextChannel] = MISSING,
        clear: bool = False,
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if channels is MISSING and not clear:
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
        self,
        ctx: RiftContext,
        *,
        roles: List[discord.Role] = MISSING,
        clear: bool = False,
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if roles is MISSING and not clear:
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
        name="verified-roles",
        brief="Modify the server's verified roles.",
        type=commands.CommandType.chat_input,
        descriptions={
            "roles": "The new verified roles, given by space separated role mentions.",
            "clear": "Set to True to clear the join roles.",
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_verified_roles(
        self,
        ctx: RiftContext,
        *,
        roles: List[discord.Role] = MISSING,
        clear: bool = False,
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if roles is MISSING and not clear:
            if settings.welcome_settings.verified_roles:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The verified roles are:\n\n{''.join(f'<@&{i}>' for i in settings.welcome_settings.verified_roles)}",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
            else:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="This server has no verified roles.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        roles_set = None if clear else [i.id for i in roles]  # type: ignore
        await settings.welcome_settings.set_(verified_roles=roles_set)
        if roles_set:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The verified roles are now:\n\n{''.join(f'<@&{i}>' for i in roles_set)}",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="The verified roles have been cleared.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

    @server_settings.command(  # type: ignore
        name="member-roles",
        brief="Modify the server's alliance member roles.",
        type=commands.CommandType.chat_input,
        descriptions={
            "roles": "The new alliance member roles, given by space separated role mentions.",
            "clear": "Set to True to clear the join roles.",
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_member_roles(
        self,
        ctx: RiftContext,
        *,
        roles: List[discord.Role] = MISSING,
        clear: bool = False,
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if roles is MISSING and not clear:
            if settings.welcome_settings.member_roles:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The member roles are:\n\n{''.join(f'<@&{i}>' for i in settings.welcome_settings.member_roles)}",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
            else:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="This server has no member roles.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        roles_set = None if clear else [i.id for i in roles]  # type: ignore
        await settings.welcome_settings.set_(member_roles=roles_set)
        if roles_set:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The member roles are now:\n\n{''.join(f'<@&{i}>' for i in roles_set)}",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="The member roles have been cleared.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

    @server_settings.command(  # type: ignore
        name="diplomat-roles",
        brief="Modify the server's diplomat roles.",
        type=commands.CommandType.chat_input,
        descriptions={
            "roles": "The new diplomat roles, given by space separated role mentions.",
            "clear": "Set to True to clear the diplomat roles.",
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_diplomat_roles(
        self,
        ctx: RiftContext,
        *,
        roles: List[discord.Role] = MISSING,
        clear: bool = False,
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if roles is MISSING and not clear:
            if settings.welcome_settings.diplomat_roles:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description=f"The diplomat roles are:\n\n{''.join(f'<@&{i}>' for i in settings.welcome_settings.diplomat_roles)}",
                        color=discord.Color.green(),
                    ),
                    ephemeral=True,
                )
            else:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="This server has no diplomat roles.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        roles_set = None if clear else [i.id for i in roles]  # type: ignore
        await settings.welcome_settings.set_(diplomat_roles=roles_set)
        if roles_set:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"The diplomat roles are now:\n\n{''.join(f'<@&{i}>' for i in roles_set)}",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="The diplomat roles have been cleared.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )

    @server_settings.command(  # type: ignore
        name="enforce-verified-nickname",
        brief="Whether or not to enforce verified nicknames.",
        type=commands.CommandType.chat_input,
        descriptions={"enforce": "Whether or not to enforce verified nicknames."},
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_enforce_verified_nickname(
        self, ctx: RiftContext, enforce: bool = MISSING
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id, "welcome_settings")
        if enforce is MISSING:
            if settings.welcome_settings.enforce_verified_nickname:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="Verified nicknames are enforced.",
                        color=discord.Color.blue(),
                    ),
                    ephemeral=True,
                )
            else:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="Verified nicknames are not enforced.",
                        color=discord.Color.blue(),
                    ),
                    ephemeral=True,
                )
        await settings.set_(enforce_verified_nickname=enforce)
        if enforce:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="Verified nicknames are now enforced.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="Verified nicknames are no longer enforced.",
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
        self, ctx: RiftContext, *, roles: List[discord.Role] = MISSING, clear: bool = False  # type: ignore
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id)
        if roles is MISSING and not clear:
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
        roles_set = None if clear else [i.id for i in roles]
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

    @server_settings.group(  # type: ignore
        name="alliance-auto-roles",
        brief="Configure alliance auto roles.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_alliance_auto_roles(self, ctx: RiftContext):
        ...

    @server_settings_alliance_auto_roles.command(  # type: ignore
        name="info",
        brief="Get information about the current alliance auto roles configuration.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_alliance_auto_roles_info(self, ctx: RiftContext):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description=f"Alliance auto roles are currently **{'enabled' if settings.welcome_settings.alliance_auto_roles_enabled else 'disabled'}** and automatic alliance auto role creation is currently **{'enabled' if settings.welcome_settings.alliance_auto_role_creation_enabled else 'disabled'}**.",
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )

    @server_settings_alliance_auto_roles.command(  # type: ignore
        name="toggle",
        brief="Toggle alliance auto roles on and off.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_alliance_auto_roles_toggle(
        self, ctx: RiftContext, enable: bool
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id)
        if enable is settings.welcome_settings.alliance_auto_roles_enabled:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"Alliance auto roles are already **{'enabled' if enable else 'disabled'}**.",
                    color=discord.Color.blue(),
                ),
                ephemeral=True,
            )
        await settings.welcome_settings.set_(alliance_auto_roles_enabled=enable)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description=f"Alliance auto roles are now **{'enabled' if enable else 'disabled'}**.",
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )

    @server_settings_alliance_auto_roles.command(  # type: ignore
        name="toggle-create",
        brief="Toggle automatically creating alliance auto roles on and off.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_alliance_auto_roles_toggle_create(
        self, ctx: RiftContext, enable: bool
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id)
        if enable is settings.welcome_settings.alliance_auto_role_creation_enabled:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"Automatic alliance auto role creation is already **{'enabled' if enable else 'disabled'}**.",
                    color=discord.Color.blue(),
                ),
                ephemeral=True,
            )
        await settings.welcome_settings.set_(alliance_auto_role_creation_enabled=enable)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description=f"Alliance auto role creation is now **{'enabled' if enable else 'disabled'}**.",
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )

    @server_settings_alliance_auto_roles.command(  # type: ignore
        name="list",
        brief="List the current alliance auto roles.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_alliance_auto_roles_list(self, ctx: RiftContext):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        settings = await GuildSettings.fetch(ctx.guild.id)
        if settings.welcome_settings.alliance_auto_roles_enabled:
            if settings.welcome_settings.alliance_auto_roles:
                roles_str = "\n".join(
                    str(i) for i in settings.welcome_settings.alliance_auto_roles
                )
                if len(roles_str) >= 4000:
                    roles_str = "\n".join(
                        f"<@&{i.role_id}> - {i.alliance_id}"
                        for i in settings.welcome_settings.alliance_auto_roles
                    )
                if len(roles_str) >= 4000:
                    await ctx.reply(
                        embed=funcs.get_embed_author_member(
                            ctx.author,
                            description="There are too alliance auto roles to display.",
                            color=discord.Color.red(),
                        ),
                        ephemeral=True,
                    )
                else:
                    await ctx.reply(
                        embed=funcs.get_embed_author_member(
                            ctx.author,
                            description=f"The alliance auto roles are:\n\n{roles_str}",
                            color=discord.Color.blue(),
                        ),
                        ephemeral=True,
                    )
            else:
                await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        description="This server has no alliance auto roles.",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="Alliance auto roles are disabled.",
                    color=discord.Color.blue(),
                ),
                ephemeral=True,
            )

    @server_settings_alliance_auto_roles.command(  # type: ignore
        name="add",
        brief="Add a role to an alliance.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_alliance_auto_roles_add(
        self, ctx: RiftContext, role: discord.Role, alliance: Alliance
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        await AllianceAutoRole.create(role, alliance)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description=f"Added {role.mention} to the {alliance.name}'s auto roles.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @server_settings_alliance_auto_roles.command(  # type: ignore
        name="remove",
        brief="Remove a role from an alliance.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_alliance_auto_roles_remove(
        self, ctx: RiftContext, role: discord.Role, alliance: Alliance
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        roles = [
            i
            for i in cache.alliance_auto_roles
            if i.role_id == role.id and i.alliance_id == alliance.id
        ]
        for r in roles:
            await r.delete()
        if roles:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description=f"Removed {role.mention} from the {alliance.name}'s auto roles.",
                    color=discord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="No alliance auto roles removed.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )

    @server_settings_alliance_auto_roles.command(  # type: ignore
        name="run",
        brief="Check and add/remove alliance auto roles.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def server_settings_alliance_auto_roles_run(self, ctx: RiftContext):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        await ctx.interaction.response.defer(ephemeral=True)
        guild = ctx.guild
        settings = await GuildSettings.fetch(guild.id)
        if not settings.welcome_settings.alliance_auto_roles_enabled:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    description="Alliance auto roles are disabled.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        auto_roles = [i for i in cache.alliance_auto_roles if i.guild_id == guild.id]
        highest_role: discord.Role = guild.get_member(self.bot.user.id).top_role  # type: ignore
        for member in guild.members:
            link = cache.get_user(member.id)
            if link is None:
                continue
            nation = cache.get_nation(link["nation_id"])
            if nation is None:
                continue
            alliance_id = nation.alliance.id if nation.alliance else None
            roles: List[discord.Role] = []
            role_ids = [i for i in auto_roles if i.alliance_id == alliance_id]
            if role_ids:
                for role_id in role_ids:
                    role = guild.get_role(role_id.role_id)
                    if role is None:
                        continue
                    if highest_role > role and role not in member.roles:
                        roles.append(role)
            elif settings.welcome_settings.alliance_auto_role_creation_enabled:
                role = await guild.create_role(
                    reason="Automatic alliance auto role creation.",
                    name=repr(nation.alliance),
                )
                roles.append(role)
            if roles:
                await member.add_roles(*roles)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description="Alliance auto roles have been updated.",
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
        guild_settings = await GuildSettings.fetch(member.guild.id, "welcome_settings")
        settings = guild_settings.welcome_settings
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
            # implement the rest of the welcome stuff below, will need to set up alliance settings and embassies first though
            if (
                settings.member_roles is not None
                and guild_settings.purpose is not None
                and nation.alliance is not None
                and guild_settings.purpose_argument is not None
            ):
                if (
                    guild_settings.purpose.startswith("ALLIANCE")
                    and nation.alliance.id == int(guild_settings.purpose_argument)
                    and nation.alliance_position
                    in {"Member", "Officer", "Heir", "Leader"}
                ):
                    for role_id in settings.member_roles:
                        role: Optional[discord.Role] = member.guild.get_role(role_id)
                        if role is None:
                            continue
                        if highest_role > role:
                            roles.append(role)
            if settings.diplomat_roles is not None and nation.alliance_position in {
                "Officer",
                "Heir",
                "Leader",
            }:
                for role_id in settings.diplomat_roles:
                    role: Optional[discord.Role] = member.guild.get_role(role_id)
                    if role is None:
                        continue
                    if highest_role > role:
                        roles.append(role)
            if settings.alliance_auto_roles_enabled:
                alliance_id = nation.alliance.id if nation.alliance else None
                auto_roles = [
                    i
                    for i in cache.alliance_auto_roles
                    if i.guild_id == member.guild.id and i.alliance_id == alliance_id
                ]
                role_ids = [i for i in auto_roles if i.alliance_id == alliance_id]
                if role_ids:
                    for role_id in role_ids:
                        role = member.guild.get_role(role_id.role_id)
                        if role is None:
                            continue
                        if highest_role > role:
                            roles.append(role)
                elif settings.alliance_auto_role_creation_enabled:
                    role = await member.guild.create_role(
                        reason="Automatic alliance auto role creation.",
                        name=repr(nation.alliance),
                    )
                    roles.append(role)
        if roles:
            await member.add_roles(*roles)
        roles = []

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.pending and not after.pending:
            await self.on_member_join(after)
        settings = await GuildWelcomeSettings.fetch(before.guild.id)
        if before.nick != after.nick and settings.enforce_verified_nickname:
            link = cache.get_user(after.id)
            if link is not None:
                nation = cache.get_nation(link["nation_id"])
                if nation is not None:
                    await settings.set_verified_nickname(after, nation)


def setup(bot: Rift):
    bot.add_cog(Settings(bot))
