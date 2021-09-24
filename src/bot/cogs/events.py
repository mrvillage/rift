from __future__ import annotations

import sys
import traceback
from asyncio import sleep
from typing import TYPE_CHECKING, List

import aiohttp
import discord
from discord.backoff import ExponentialBackoff
from discord.ext import commands

from ... import funcs
from ...cache import cache
from ...checks import has_manage_permissions
from ...data.classes import Alliance, Subscription
from ...env import SOCKET_IP, SOCKET_PORT
from ...ref import Rift


class Events(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot
        self.bot.loop.create_task(self.socket())

    async def socket(self):
        backoff = ExponentialBackoff()
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(
                        f"ws://{SOCKET_IP}:{SOCKET_PORT}", max_msg_size=0, timeout=300
                    ) as ws:
                        print("rift-data socket connected", flush=True)
                        async for message in ws:
                            data = message.json()
                            if "event" in data:
                                self.bot.dispatch(data["event"], **data["data"])
            except ConnectionRefusedError:
                print("rift-data socket refused", flush=True)
                delay = backoff.delay()
                await sleep(delay)
            except Exception as error:
                print("rift-data socket connection error", file=sys.stderr, flush=True)
                traceback.print_exception(
                    type(error), error, error.__traceback__, file=sys.stderr
                )
                delay = backoff.delay()
                await sleep(delay)

    @commands.group(
        name="subscribe",
        help="Subscribe to an event stream. Note: Not all types are valid for every event.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe(
        self,
        ctx: commands.Context,
    ):
        ...

    @subscribe.group(name="nation", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_nation(self, ctx: commands.Context):
        ...

    @subscribe_nation.command(name="create", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_nation_create(self, ctx: commands.Context):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(ctx.channel, "NATION", "CREATE")
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `NATION_CREATE` events.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe_nation.command(name="delete", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_nation_delete(self, ctx: commands.Context):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(ctx.channel, "NATION", "DELETE")
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `NATION_DELETE` events.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe_nation.command(name="update", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_nation_update(
        self,
        ctx: commands.Context,
        changes: List[str],
        alliances: List[Alliance] = [],
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        changes = [
            u
            for i in changes
            if (u := i.upper())
            in {
                "ALLIANCE_POSITION",
                "ALLIANCE_POSITION_ALL",
                "ALLIANCE",
                "VACATION_MODE",
            }
        ]
        if not changes:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You didn't give any valid changes!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        subscription = await Subscription.subscribe(
            ctx.channel, "NATION", "UPDATE", changes, [i.id for i in alliances]
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `NATION_UPDATE` events for the following changes: {', '.join('`' + i + '`' for i in changes)} for {'the following' if alliances else 'all'} alliances{(': ' + ', '.join(repr(i) for i in alliances)) if alliances else ''}.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe.group(name="alliance", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_alliance(self, ctx: commands.Context):
        ...

    @subscribe_alliance.command(name="create", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_alliance_create(self, ctx: commands.Context):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(ctx.channel, "ALLIANCE", "CREATE")
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `ALLIANCE_CREATE` events.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe_alliance.command(name="delete", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_alliance_delete(self, ctx: commands.Context):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(ctx.channel, "ALLIANCE", "DELETE")
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `ALLIANCE_DELETE` events.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe.group(name="treaty", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_treaty(self, ctx: commands.Context):
        ...

    @subscribe_alliance.command(name="create", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_treaty_create(self, ctx: commands.Context):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(ctx.channel, "TREATY", "CREATE")
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `TREATY_CREATE` events.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe_alliance.command(name="delete", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_treaty_delete(self, ctx: commands.Context):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(ctx.channel, "TREATY", "DELETE")
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `TREATY_DELETE` events.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @commands.group(name="subscription", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscription(self, ctx: commands.Context):
        ...

    @subscription.command(name="list", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscription_list(
        self, ctx: commands.Context, channel: discord.TextChannel = None
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        if channel is None:
            subscriptions = [
                i for i in cache.subscriptions if i.guild_id == ctx.guild.id
            ]
        else:
            subscriptions = [
                i for i in cache.subscriptions if i.channel_id == channel.id
            ]
        if not subscriptions:
            if channel is None:
                return await ctx.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        "There are no subscriptions for this server!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"There are no subscriptions for {channel.mention}.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        if channel is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"There are {len(subscriptions):,} on this server.\n\n"
                    + "\n".join(
                        f"`{i.category}_{i.type}` - <#{i.channel_id}> - {i.id}"
                        for i in subscriptions
                    ),
                    color=discord.Color.blue(),
                )
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"There are {len(subscriptions):,} in {channel.mention}.\n\n"
                + "\n".join(f"`{i.category}_{i.type}` - {i.id}" for i in subscriptions),
                color=discord.Color.blue(),
            )
        )

    @subscription.command(name="info", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscription_info(
        self, ctx: commands.Context, subscription: Subscription
    ):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Subscription ID: {subscription.id}\nEvent: {subscription.category}_{subscription.type}\nSubtypes: {', '.join(subscription.sub_types) if subscription.sub_types else 'None'}\nArguments: {', '.join(str(i) for i in subscription.arguments) if subscription.arguments else 'None'}",
                color=discord.Color.blue(),
            )
        )

    @subscription.command(name="delete", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscription_delete(
        self, ctx: commands.Context, subscription: Subscription
    ):
        await subscription.delete()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Subscription {subscription.id} has been deleted.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )


def setup(bot: Rift):
    bot.add_cog(Events(bot))
