from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...checks import has_manage_permissions
from ...data.classes import Alliance, Embassy, EmbassyConfig, Nation
from ...ref import Rift, RiftContext

if TYPE_CHECKING:
    from _typings import EmbassyConfigData, EmbassyData


class Embassies(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="embassy",
        case_insensitive=True,
        brief="A group of commands related to embassies.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    async def embassy(self, ctx: RiftContext):
        ...

    @embassy.group(  # type: ignore
        name="config",
        brief="A group of commands related to embassy configuration.",
        case_insensitive=True,
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def embassy_config(self, ctx: RiftContext):
        ...

    @embassy_config.command(  # type: ignore
        name="create",
        brief="Create an embassy configuration.",
        type=commands.CommandType.chat_input,
        descriptions={
            "start": "The starting message when an embassy is created.",
            "category": "The category to create the embassy in.",
        },
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def embassy_config_create(
        self,
        ctx: RiftContext,
        start: str,
        category: discord.CategoryChannel = MISSING,
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        category = category or None
        data = {
            "category_id": category.id if category else None,
            "guild_id": ctx.guild.id,
            "start_message": start,
        }
        if TYPE_CHECKING:
            assert isinstance(data, EmbassyConfigData)
        config = EmbassyConfig(data)
        await config.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Embassy Configuration {config.id} created.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @embassy_config.command(  # type: ignore
        name="list",
        brief="List the embassy configurations in the server.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def embassy_config_list(self, ctx: RiftContext):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        configs = [i for i in cache.embassy_configs if i.guild_id == ctx.guild.id]
        if not configs:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "No embassy configurations found for this server.",
                    discord.Color.red(),
                ),
                ephemeral=True,
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(
                    f"{config.id} - {ctx.guild.get_channel(config.category_id or 0)}"
                    for config in configs
                ),
                color=discord.Color.green(),
            )
        )

    @embassy_config.command(  # type: ignore
        name="claim",
        brief="Claim a channel for an alliance in an embassy configuration.",
        type=commands.CommandType.chat_input,
        descriptions={
            "config": "The embassy config to claim under.",
            "alliance": "The alliance to claim the embassy for.",
            "channel": "The channel to claim.",
        },
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def embassy_config_claim(
        self,
        ctx: RiftContext,
        config: EmbassyConfig,
        *,
        alliance: Alliance,
        channel: discord.TextChannel = MISSING,
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild) and isinstance(
                ctx.channel, discord.TextChannel
            )
        channel = channel or ctx.channel
        data = {
            "id": channel.id,
            "alliance_id": alliance.id,
            "config_id": config.id,
            "guild_id": ctx.guild.id,
            "open": True,
        }
        if TYPE_CHECKING:
            assert isinstance(data, EmbassyData)
        embassy = Embassy(data)
        await embassy.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"{channel.mention} claimed for {repr(alliance)} under embassy configuration {config.id}.",
            ),
            ephemeral=True,
        )

    @embassy.command(  # type: ignore
        name="open", brief="Open an embassy.", type=commands.CommandType.chat_input
    )
    @commands.guild_only()
    async def embassy_open(self, ctx: RiftContext, config: EmbassyConfig):
        if TYPE_CHECKING:
            assert isinstance(ctx.author, discord.Member)
        await ctx.interaction.response.defer()
        nation = await Nation.convert(ctx, None)
        if nation.alliance_position not in {"Officer", "Heir", "Leader"}:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You must be an Officer or higher to create an embassy.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if nation.alliance is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You must be in an alliance to create an embassy.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        embassy, start = await config.create(ctx.author, nation.alliance)
        if start:
            await embassy.start(ctx.author, config)
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, f"Embassy:\n<#{embassy.id}>"
                ),
                ephemeral=True,
            )


def setup(bot: Rift) -> None:
    bot.add_cog(Embassies(bot))
