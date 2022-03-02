from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...checks import has_manage_permissions
from ...data.classes import Ticket, TicketConfig
from ...errors import EmbedErrorMessage
from ...ref import Rift, RiftContext


class Tickets(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="ticket",
        brief="A group of commands related to tickets.",
        case_insensitive=True,
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    async def ticket(self, ctx: RiftContext):
        ...

    @ticket.command(  # type: ignore
        name="archive",
        brief="Archive a ticket.",
        type=commands.CommandType.chat_input,
        descriptions={
            "channel": "The channel of the ticket to archive, defaults to the current channel.",
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def ticket_archive(
        self, ctx: RiftContext, channel: discord.TextChannel = MISSING
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
        channel = channel or ctx.channel
        try:
            ticket = await Ticket.fetch(ctx.channel.id)
        except IndexError:
            raise EmbedErrorMessage(
                ctx.author,
                "This channel is not a ticket.",
            )
        if not ticket.open:
            raise EmbedErrorMessage(
                ctx.author,
                "This ticket is already archived!",
            )
        config = await TicketConfig.fetch(ticket.config_id)
        ticket.open = False
        await ticket.save()
        category = self.bot.get_channel(config.archive_category_id) or ctx.channel.category  # type: ignore
        if TYPE_CHECKING:
            assert isinstance(category, discord.CategoryChannel) or category is None
            assert isinstance(ctx.channel, discord.TextChannel)
        name = f"archived-{ctx.channel.name}"
        if len(name) > 100:
            name = f"archived-{ticket.ticket_number}"
        await ctx.channel.edit(name=name, category=category, sync_permissions=True)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Ticket `{ctx.channel.id}` has been archived.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @ticket.group(  # type: ignore
        name="config",
        brief="A group of commands related to ticket configurations.",
        case_insensitive=True,
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def ticket_config(self, ctx: RiftContext):
        ...

    @ticket_config.command(  # type: ignore
        name="create",
        brief="Create a new ticket configuration.",
        type=commands.CommandType.chat_input,
        descriptions={
            "start": "The starting message for tickets created.",
            "category": "The category to make tickets in, defaults to no category.",
            "archive_category": "The category to archive tickets in, defaults to the category of the channel at archive.",
            "mentions": "The users and roles to mention on ticket creation, given by space separated user and role mentions.",
        },
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def ticket_config_create(
        self,
        ctx: RiftContext,
        start: str,
        category: discord.CategoryChannel = MISSING,
        archive_category: discord.CategoryChannel = MISSING,
        mentions: List[Union[discord.Member, discord.User, discord.Role]] = MISSING,
    ):
        mentions = mentions or []
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        config = TicketConfig(
            {
                "id": 0,
                "category": category.id if category else None,
                "guild": ctx.guild.id,
                "start_message": start,
                "archive_category": (archive_category and archive_category.id) or None,
                "role_mentions": [
                    i.id for i in mentions if isinstance(i, discord.Role)
                ],
                "user_mentions": [
                    i.id
                    for i in mentions
                    if isinstance(i, (discord.Member, discord.User))
                ],
            }
        )
        await config.save()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Ticket Configuration {config.id} created.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @ticket_config.command(  # type: ignore
        name="list",
        brief="List the embassy configurations in the server.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def ticket_config_list(self, ctx: RiftContext):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        configs = [i for i in cache.ticket_configs if i.guild_id == ctx.guild.id]
        if not configs:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "No ticket configurations found for this server.",
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

    @ticket.command(  # type: ignore
        name="open", brief="Open a ticket.", type=commands.CommandType.chat_input
    )
    @commands.guild_only()
    async def ticket_open(self, ctx: RiftContext, config: TicketConfig):
        if TYPE_CHECKING:
            assert isinstance(ctx.author, discord.Member)
        await ctx.interaction.response.defer()
        ticket = await config.create(ctx.author)
        await ticket.start(ctx.author, config)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author, f"Ticket Created!\n<#{ticket.id}>"
            ),
            ephemeral=True,
        )


def setup(bot: Rift) -> None:
    bot.add_cog(Tickets(bot))
