from __future__ import annotations

import sys
import traceback
from asyncio import sleep
from typing import TYPE_CHECKING, List

import aiohttp
import discord
from discord.backoff import ExponentialBackoff
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...checks import has_manage_permissions
from ...data.classes import Condition, Forum, Subscription
from ...env import SOCKET_IP, SOCKET_PORT
from ...errors import EmbedErrorMessage
from ...ref import Rift, RiftContext


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
            except (
                ConnectionRefusedError,
                aiohttp.ClientConnectorError,
            ) as error:
                print("rift-data socket refused", file=sys.stderr, flush=True)
                traceback.print_exception(
                    type(error), error, error.__traceback__, file=sys.stderr
                )
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
        brief="Subscribe to an event stream.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe(
        self,
        ctx: RiftContext,
    ):
        ...

    @subscribe.group(name="nation", type=commands.CommandType.chat_input)  # type: ignore
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_nation(self, ctx: RiftContext):
        ...

    @subscribe_nation.command(  # type: ignore
        name="create",
        brief="Subscribe to NATION_CREATE events in this channel.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to evaluate to determine whether to send the event or not."
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_nation_create(
        self, ctx: RiftContext, condition: Condition = MISSING
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(
            ctx.channel, "NATION", "CREATE", condition=condition
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `NATION_CREATE` events with {'' if condition else 'no '}condition{' `' + str(condition) + '`' if condition else ''}.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe_nation.command(  # type: ignore
        name="delete",
        brief="Subscribe to NATION_DELETE events in this channel.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to evaluate to determine whether to send the event or not."
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_nation_delete(
        self, ctx: RiftContext, condition: Condition = MISSING
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(
            ctx.channel, "NATION", "DELETE", condition=condition
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `NATION_DELETE` events with {'' if condition else 'no '}condition{' `' + str(condition) + '`' if condition else ''}.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe_nation.command(  # type: ignore
        name="update",
        brief="Subscribe to NATION_UPDATE events in this channel.",
        type=commands.CommandType.chat_input,
        descriptions={
            "changes": "A space separated list of changes. ALLIANCE_POSITION, ALLIANCE_POSITION_ALL, ALLIANCE, VACATION_MODE",
            "condition": "The condition to evaluate to determine whether to send the event or not.",
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_nation_update(
        self,
        ctx: RiftContext,
        changes: List[str],
        condition: Condition = MISSING,
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
            raise EmbedErrorMessage(
                ctx.author,
                "You didn't give any valid changes!",
            )
        subscription = await Subscription.subscribe(
            ctx.channel, "NATION", "UPDATE", changes, condition=condition
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `NATION_UPDATE` events for the following changes: {', '.join('`' + i + '`' for i in changes)} with {'' if condition else 'no '}condition{' `' + str(condition) + '`' if condition else ''}.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe.group(name="alliance", type=commands.CommandType.chat_input)  # type: ignore
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_alliance(self, ctx: RiftContext):
        ...

    @subscribe_alliance.command(  # type: ignore
        name="create",
        brief="Subscribe to ALLIANCE_CREATE events in this channel.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to evaluate to determine whether to send the event or not."
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_alliance_create(
        self, ctx: RiftContext, condition: Condition = MISSING
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(
            ctx.channel, "ALLIANCE", "CREATE", condition=condition
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `ALLIANCE_CREATE` events with {'' if condition else 'no '}condition{' `' + str(condition) + '`' if condition else ''}.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe_alliance.command(  # type: ignore
        name="delete",
        brief="Subscribe to ALLIANCE_DELETE events in this channel.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to evaluate to determine whether to send the event or not."
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_alliance_delete(
        self, ctx: RiftContext, condition: Condition = MISSING
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(
            ctx.channel, "ALLIANCE", "DELETE", condition=condition
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `ALLIANCE_DELETE` events with {'' if condition else 'no '}condition{' `' + str(condition) + '`' if condition else ''}.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe.group(name="treaty", type=commands.CommandType.chat_input)  # type: ignore
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_treaty(self, ctx: RiftContext):
        ...

    @subscribe_treaty.command(  # type: ignore
        name="create",
        brief="Subscribe to TREATY_CREATE events in this channel.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_treaty_create(self, ctx: RiftContext):
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

    @subscribe_treaty.command(  # type: ignore
        name="delete",
        brief="Subscribe to TREATY_DELETE events in this channel.",
        type=commands.CommandType.chat_input,
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_treaty_delete(self, ctx: RiftContext):
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

    @subscribe.group(name="forum-post", type=commands.CommandType.chat_input)  # type: ignore
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_forum_post(self, ctx: RiftContext):
        ...

    @subscribe_forum_post.command(  # type: ignore
        name="create",
        brief="Subscribe to FORUM_POST_CREATE events in this channel.",
        type=commands.CommandType.chat_input,
        descriptions={
            "forums": "Space separated list of any of: ALLIANCE_AFFAIRS, ORBIS_CENTRAL."
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_forum_post_create(
        self,
        ctx: RiftContext,
        forums: List[Forum],
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        if not forums:
            raise EmbedErrorMessage(
                ctx.author,
                "You didn't give any valid forums!",
            )
        subscription = await Subscription.subscribe(
            ctx.channel,
            "FORUM_POST",
            "CREATE",
            [i.name.upper().replace(" ", "_") for i in forums],
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `FORUM_POST_CREATE` events for the following forums: {', '.join('`' + i.name.upper().replace(' ', '_') + '`' for i in forums)}.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @subscribe.group(name="war", type=commands.CommandType.chat_input)  # type: ignore
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_war(self, ctx: RiftContext):
        ...

    @subscribe_war.command(  # type: ignore
        name="create",
        brief="Subscribe to WAR_CREATE events in this channel.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to evaluate to determine whether to send the event or not."
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscribe_war_create(
        self, ctx: RiftContext, condition: Condition = MISSING
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.channel, discord.TextChannel)
            assert isinstance(ctx.author, discord.Member)
        subscription = await Subscription.subscribe(
            ctx.channel, "WAR", "CREATE", condition=condition
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Successfully subscribed to `WAR_CREATE` events with {'' if condition else 'no '}condition{' `' + str(condition) + '`' if condition else ''}.\nSubscription ID: {subscription.id}",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @commands.group(name="subscription", type=commands.CommandType.chat_input)
    @has_manage_permissions()
    @commands.guild_only()
    async def subscription(self, ctx: RiftContext):
        ...

    @subscription.command(  # type: ignore
        name="list",
        brief="List the subscriptions for this server or a channel.",
        type=commands.CommandType.chat_input,
        descriptions={
            "channel": "The channel to list subscriptions of, defaults to the server."
        },
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscription_list(
        self, ctx: RiftContext, channel: discord.TextChannel = MISSING
    ):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        if channel is MISSING:
            subscriptions = [
                i for i in cache.subscriptions if i.guild_id == ctx.guild.id
            ]
        elif channel.guild.id != ctx.guild.id:
            raise EmbedErrorMessage(
                ctx.author,
                "You can only list subscriptions for this server.",
            )
        else:
            subscriptions = [
                i for i in cache.subscriptions if i.channel_id == channel.id
            ]
        if not subscriptions:
            if channel is MISSING:
                raise EmbedErrorMessage(
                    ctx.author,
                    "There are no subscriptions for this server!",
                )
            raise EmbedErrorMessage(
                ctx.author,
                f"There are no subscriptions for {channel.mention}.",
            )
        if channel is MISSING:
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

    @subscription.command(  # type: ignore
        name="info",
        brief="Get info on a subscription.",
        type=commands.CommandType.chat_input,
        descriptions={"subscription": "The subscription to get info on."},
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscription_info(self, ctx: RiftContext, subscription: Subscription):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Subscription ID: {subscription.id}\nEvent: {subscription.category}_{subscription.type}\nSubtypes: {', '.join(subscription.sub_types) if subscription.sub_types else 'None'}\nCondition: {subscription.condition}",
                color=discord.Color.blue(),
            )
        )

    @subscription.command(  # type: ignore
        name="delete",
        brief="Delete a subscription.",
        type=commands.CommandType.chat_input,
        descriptions={"subscription": "The subscription to delete."},
    )
    @has_manage_permissions()
    @commands.guild_only()
    async def subscription_delete(self, ctx: RiftContext, subscription: Subscription):
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
