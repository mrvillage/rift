from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from ... import funcs
from ...checks import has_manage_permissions
from ...data.classes import TicketConfig
from ...data.query import query_ticket_config_by_guild
from ...ref import Rift

if TYPE_CHECKING:
    from typings import TicketConfigData


class Tickets(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="ticket",
        help="A group of commands related to tickets.",
        case_insensitive=True,
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    async def ticket(self, ctx: commands.Context):
        ...

    @ticket.group(
        name="config",
        help="A group of commands related to ticket configurations.",
        case_insensitive=True,
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def ticket_config(self, ctx: commands.Context):
        ...

    @ticket_config.command(
        name="create",
        help="Create a new ticket configuration.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def ticket_config_create(
        self,
        ctx: commands.Context,
        start: str,
        category: discord.CategoryChannel = None,
    ):
        data = {
            "config_id": ctx.interaction.id,
            "category_id": category and category.id,
            "guild_id": ctx.guild.id,
            "start_message": start,
        }
        if TYPE_CHECKING:
            assert isinstance(data, TicketConfigData)
        config = TicketConfig(data)
        await config.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Ticket Configuration {config.config_id} created.",
                color=discord.Color.green(),
            )
        )

    @ticket_config.command(
        name="list",
        help="List the embassy configurations in the server.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def ticket_config_list(self, ctx: commands.Context):
        configs = [
            TicketConfig(config)
            for config in await query_ticket_config_by_guild(ctx.guild.id)
        ]
        if not configs:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "No ticket configurations found for this guild.",
                    discord.Color.red(),
                )
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(
                    f"{config.config_id} - {ctx.guild.get_channel(config.category_id).name if config.category_id else None}"
                    for config in configs
                ),
                color=discord.Color.green(),
            )
        )


def setup(bot: Rift) -> None:
    bot.add_cog(Tickets(bot))
