from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from ... import funcs
from ...checks import has_manage_permissions
from ...data.classes import Alliance, Embassy, EmbassyConfig
from ...data.query import query_embassy_config_by_guild
from ...ref import Rift

if TYPE_CHECKING:
    from typings import EmbassyConfigData, EmbassyData


class Embassies(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(name="embassy")
    @commands.guild_only()
    async def embassy(self, ctx: commands.Context):
        ...

    @embassy.group(name="config")
    @commands.guild_only()
    @has_manage_permissions()
    async def embassy_config(self, ctx: commands.Context):
        ...

    @embassy_config.command(name="create")
    @commands.guild_only()
    @has_manage_permissions()
    async def embassy_config_create(
        self, ctx: commands.Context, category, *, start: str
    ):
        if category.lower() == "none":
            category = None
        else:
            category = await commands.CategoryChannelConverter().convert(ctx, category)
        if TYPE_CHECKING:
            assert isinstance(ctx.message, discord.Message)
        data = {
            "config_id": ctx.message.id,
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
                f"Embassy Configuration {config.config_id} created.",
                color=discord.Color.green(),
            )
        )

    @embassy_config.command(name="list")
    @commands.guild_only()
    @has_manage_permissions()
    async def embassy_config_list(self, ctx: commands.Context):
        if TYPE_CHECKING:
            assert isinstance(ctx.message, discord.Message)
        configs = [
            EmbassyConfig(config)
            for config in await query_embassy_config_by_guild(ctx.guild.id)
        ]
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
                    f"{config.config_id} - {ctx.guild.get_channel(config.category_id).name}"
                    for config in configs
                ),
                color=discord.Color.green(),
            )
        )

    @embassy_config.command(name="claim")
    @commands.guild_only()
    @has_manage_permissions()
    async def embassy_config_claim(
        self, ctx: commands.Context, config: EmbassyConfig, *, alliance: Alliance
    ):
        data = {
            "embassy_id": ctx.channel.id,
            "alliance_id": alliance.id,
            "config_id": config.config_id,
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
                f"{ctx.channel.mention} claimed for {repr(alliance)} under embassy configuration {config.config_id}.",
            )
        )


def setup(bot: Rift) -> None:
    bot.add_cog(Embassies(bot))
