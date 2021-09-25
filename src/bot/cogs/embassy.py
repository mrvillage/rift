from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from ... import funcs
from ...cache import cache
from ...checks import has_manage_permissions
from ...data.classes import Alliance, Embassy, EmbassyConfig
from ...ref import Rift

if TYPE_CHECKING:
    from typings import EmbassyConfigData, EmbassyData


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
    async def embassy(self, ctx: commands.Context):
        ...

    @embassy.group(
        name="config",
        brief="A group of commands related to embassy configuration.",
        case_insensitive=True,
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def embassy_config(self, ctx: commands.Context):
        ...

    @embassy_config.command(
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
        ctx: commands.Context,
        start: str,
        category: discord.CategoryChannel = None,
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        data = {
            "id": ctx.interaction.id,
            "category_id": category and category.id,
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

    @embassy_config.command(
        name="list",
        brief="List the embassy configurations in the server.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def embassy_config_list(self, ctx: commands.Context):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        configs = [i for i in cache.embassy_configs if i.guild_id == ctx.guild.id]
        if not configs:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "No embassy configurations found for this guild.",
                    discord.Color.red(),
                )
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(
                    f"{config.id} - {category}"
                    for config in configs
                    if config.category_id
                    and (category := ctx.guild.get_channel(config.category_id))
                ),
                color=discord.Color.green(),
            )
        )

    @embassy_config.command(
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
        ctx: commands.Context,
        config: EmbassyConfig,
        *,
        alliance: Alliance,
        channel: discord.TextChannel = None,
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


def setup(bot: Rift) -> None:
    bot.add_cog(Embassies(bot))
