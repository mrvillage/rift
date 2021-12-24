from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, List, Union

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...data.classes import Condition, Nation, TargetReminder
from ...ref import Rift, RiftContext


class TargetContext:
    def __init__(self, author: discord.User, guild: discord.Guild):
        self.author = author
        self.guild = guild


class Targets(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="target",
        brief="A group of commands to manage targets",
        type=commands.CommandType.chat_input,
    )
    async def target(self, ctx: RiftContext):
        ...

    @target.group(  # type: ignore
        name="reminder",
        brief="A group of commands to manage target reminders",
        type=commands.CommandType.chat_input,
    )
    async def target_reminder(self, ctx: RiftContext):
        ...

    @target_reminder.command(  # type: ignore
        name="add",
        brief="Add a target reminder.",
        type=commands.CommandType.chat_input,
        descriptions={
            "nation": "The nation to add.",
            "channels": "The channels to send notifications in.",
            "mentions": "The roles and users to mention when a notification comes.",
            "direct_message": "Whether or not to send a Direct Message as a notification.",
        },
    )
    async def target_reminder_add(
        self,
        ctx: RiftContext,
        *,
        nation: Nation,
        channels: List[discord.TextChannel] = [],
        mentions: List[Union[discord.Member, discord.User, discord.Role]] = [],
        direct_message: bool = False,
    ):
        if not channels and not direct_message:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You need to specify channels to send in or specify to Direct Message you!",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        reminder = await TargetReminder.create(
            nation,
            ctx.author,
            channels,
            [i for i in mentions if isinstance(i, discord.Role)],
            [i for i in mentions if isinstance(i, (discord.Member, discord.User))],
            direct_message,
        )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Target Reminder #{reminder.id} has been added. It will mention {reminder.mentions} in {' '.join(i.mention for i in channels)} and will {'' if direct_message else 'not'} Direct Message you when {repr(nation)} comes off beige.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @target_reminder.command(  # type: ignore
        name="remove",
        brief="Remove a target reminder.",
        type=commands.CommandType.chat_input,
        descriptions={
            "reminder": "The target reminder to remove.",
        },
    )
    async def target_reminder_remove(
        self, ctx: RiftContext, *, reminder: TargetReminder
    ):
        await reminder.delete()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Target Reminder #{reminder.id} has been removed.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @target_reminder.command(  # type: ignore
        name="list",
        brief="List all your target reminders.",
        type=commands.CommandType.chat_input,
    )
    async def target_reminder_list(self, ctx: RiftContext):
        reminders = sorted(
            (i for i in cache.target_reminders if i.owner_id == ctx.author.id),
            key=lambda x: x.id,
        )
        if not reminders:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "You have no target reminders.",
                    color=discord.Color.red(),
                ),
                ephemeral=True,
            )
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(
                    f"**#{i.id}**: [{repr(i.nation)}](https://politicsandwar.com/nation/id={i.nation.id if i.nation else 0})"
                    for i in reminders
                ),
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )

    @target_reminder.command(  # type: ignore
        name="info",
        brief="Get information about a target.",
        type=commands.CommandType.chat_input,
        descriptions={
            "reminder": "The target reminder to remove.",
        },
    )
    async def target_reminder_info(self, ctx: RiftContext, reminder: TargetReminder):
        channel_mentions = " ".join(f"<#{i}>" for i in reminder.channel_ids)
        mentions = reminder.mentions
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                inspect.cleandoc(
                    f"""
                Target Reminder #{reminder.id}:
                Nation: {repr(reminder.nation)}
                Channels: {channel_mentions or None}
                Mentions: {mentions if len(mentions) > 1 else None}
                Direct Message: {reminder.direct_message}
                """
                ),
                color=discord.Color.blue(),
            ),
            ephemeral=True,
        )

    @commands.Cog.listener()
    async def on_nation_update(self, before: Nation, after: Nation):
        if before.color != "Beige" or after.color == "Beige":
            return
        reminders = [i for i in cache.target_reminders if i.nation is after]
        if not reminders:
            return
        for reminder in reminders:
            for channel_id in reminder.channel_ids:
                channel = self.bot.get_channel(channel_id)
                if channel is None:
                    continue
                if TYPE_CHECKING:
                    assert isinstance(channel, discord.TextChannel)
                embed = after.get_info_embed(TargetContext(self.bot.get_user(reminder.owner_id), channel.guild))  # type: ignore
                await channel.send(
                    content=f"{repr(after)} is no longer on beige!\n{reminder.mentions}",
                    embed=embed,
                )
            if reminder.direct_message:
                owner = self.bot.get_user(reminder.owner_id)
                if owner is None:
                    continue
                await owner.send(
                    content=f"{repr(after)} is no longer on beige!",
                    embed=after.get_info_embed(TargetContext(owner, None)),  # type: ignore
                )

    @target.group(  # type: ignore
        name="find", brief="Find war targets.", type=commands.CommandType.chat_input
    )
    async def target_find(self, ctx: RiftContext):
        ...

    @target_find.command(  # type: ignore
        name="custom",
        brief="Find war targets.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to evaluate to determine target validity.",
            "nation": "The nation to find targets for, defaults to yourself.",
            "count_cities": "Whether to count cities when rating, defaults to true.",
            "count_loot": "Whether to count the nation's estimated loot when rating, defaults to false.",
            "count_infrastructure": "Whether to count the nation's infrastructure when rating, defaults to false.",
            "count_military": "Whether to count the nation's military when rating, defaults to false.",
            "count_activity": "Whether to count the nation's last activity when rating, defaults to false.",
            "evaluate_alliance_raid_default": "Whether to evaluate your alliance's default raid condition, defaults to false.",
            "evaluate_alliance_nuke_default": "Whether to evaluate your alliance's default nuke condition, defaults to false.",
            "eval_alliance_military_default": "Whether to evaluate your alliance's default military condition, defaults to false.",
            "offset": "The offset of targets to display, defaults to 0 (starts at the top target).",
            "attack": "Whether to attack the nation rather than find attacks for it (ignores loot), defaults to false.",
        },
    )
    async def target_find_custom(
        self,
        ctx: RiftContext,
        condition: Condition = MISSING,
        nation: Nation = MISSING,
        count_cities: bool = True,
        count_loot: bool = False,
        count_infrastructure: bool = False,
        count_military: bool = False,
        count_activity: bool = False,
        evaluate_alliance_raid_default: bool = False,
        evaluate_alliance_nuke_default: bool = False,
        eval_alliance_military_default: bool = False,
        offset: int = 0,
        attack: bool = False,
    ):
        if attack:
            await funcs.find_attackers(
                ctx,
                condition,
                nation,
                count_cities=count_cities,
                count_infrastructure=count_infrastructure,
                count_military=count_military,
                count_activity=count_activity,
                evaluate_alliance_raid_default=evaluate_alliance_raid_default,
                evaluate_alliance_nuke_default=evaluate_alliance_nuke_default,
                evaluate_alliance_military_default=eval_alliance_military_default,
                offset=offset,
            )
        else:
            await funcs.find_targets(
                ctx,
                condition,
                nation,
                count_cities=count_cities,
                count_loot=count_loot,
                count_infrastructure=count_infrastructure,
                count_military=count_military,
                count_activity=count_activity,
                evaluate_alliance_raid_default=evaluate_alliance_raid_default,
                evaluate_alliance_nuke_default=evaluate_alliance_nuke_default,
                evaluate_alliance_military_default=eval_alliance_military_default,
                offset=offset,
            )

    @target_find.command(  # type: ignore
        name="raid",
        brief="Find raid targets.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to evaluate to determine target validity.",
            "nation": "The nation to find targets for, defaults to yourself.",
            "count_infrastructure": "Whether to count the nation's infrastructure when rating, defaults to false.",
            "evaluate_alliance_raid_default": "Whether to evaluate your alliance's default raid condition, defaults to true.",
            "offset": "The offset of targets to display, defaults to 0 (starts at the top target).",
            "attack": "Whether to attack the nation rather than find attacks for it (ignores loot), defaults to false.",
        },
    )
    async def target_find_raid(
        self,
        ctx: RiftContext,
        condition: Condition = MISSING,
        nation: Nation = MISSING,
        count_infrastructure: bool = False,
        evaluate_alliance_raid_default: bool = True,
        offset: int = 0,
        attack: bool = False,
    ):
        if attack:
            await funcs.find_attackers(
                ctx,
                condition,
                nation,
                count_cities=True,
                count_infrastructure=count_infrastructure,
                count_military=True,
                count_activity=True,
                evaluate_alliance_raid_default=evaluate_alliance_raid_default,
                offset=offset,
            )
        else:
            await funcs.find_targets(
                ctx,
                condition,
                nation,
                count_cities=True,
                count_loot=True,
                count_infrastructure=count_infrastructure,
                count_military=True,
                count_activity=True,
                evaluate_alliance_raid_default=evaluate_alliance_raid_default,
                offset=offset,
            )

    @target_find.command(  # type: ignore
        name="nuke",
        brief="Find nuke targets.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to evaluate to determine target validity.",
            "nation": "The nation to find targets for, defaults to yourself.",
            "count_loot": "Whether to count the nation's estimated loot when rating, defaults to false.",
            "count_military": "Whether to count the nation's military when rating, defaults to false.",
            "count_activity": "Whether to count the nation's last activity when rating, defaults to false.",
            "evaluate_alliance_nuke_default": "Whether to evaluate your alliance's default nuke condition, defaults to true.",
            "offset": "The offset of targets to display, defaults to 0 (starts at the top target).",
            "attack": "Whether to attack the nation rather than find attacks for it (ignores loot), defaults to false.",
        },
    )
    async def target_find_nuke(
        self,
        ctx: RiftContext,
        condition: Condition = MISSING,
        nation: Nation = MISSING,
        count_loot: bool = False,
        count_military: bool = False,
        count_activity: bool = False,
        evaluate_alliance_nuke_default: bool = True,
        offset: int = 0,
        attack: bool = False,
    ):
        if attack:
            await funcs.find_attackers(
                ctx,
                condition,
                nation,
                count_cities=False,
                count_infrastructure=True,
                count_military=count_military,
                count_activity=count_activity,
                evaluate_alliance_nuke_default=evaluate_alliance_nuke_default,
                offset=offset,
            )
        else:
            await funcs.find_targets(
                ctx,
                condition,
                nation,
                count_cities=False,
                count_loot=count_loot,
                count_infrastructure=True,
                count_military=count_military,
                count_activity=count_activity,
                evaluate_alliance_nuke_default=evaluate_alliance_nuke_default,
                offset=offset,
            )

    @target_find.command(  # type: ignore
        name="military",
        brief="Find military war targets.",
        type=commands.CommandType.chat_input,
        descriptions={
            "condition": "The condition to evaluate to determine target validity.",
            "nation": "The nation to find targets for, defaults to yourself.",
            "count_cities": "Whether to count cities when rating, defaults to true.",
            "count_loot": "Whether to count the nation's estimated loot when rating, defaults to false.",
            "count_infrastructure": "Whether to count the nation's infrastructure when rating, defaults to false.",
            "count_activity": "Whether to count the nation's last activity when rating, defaults to false.",
            "eval_alliance_military_default": "Whether to evaluate your alliance's default military condition, defaults to true.",
            "offset": "The offset of targets to display, defaults to 0 (starts at the top target).",
            "attack": "Whether to attack the nation rather than find attacks for it (ignores loot), defaults to false.",
        },
    )
    async def target_find_military(
        self,
        ctx: RiftContext,
        condition: Condition = MISSING,
        nation: Nation = MISSING,
        count_cities: bool = True,
        count_loot: bool = False,
        count_infrastructure: bool = False,
        count_activity: bool = False,
        eval_alliance_military_default: bool = True,
        offset: int = 0,
        attack: bool = False,
    ):
        if attack:
            await funcs.find_attackers(
                ctx,
                condition,
                nation,
                count_cities=count_cities,
                count_infrastructure=count_infrastructure,
                count_military=True,
                count_activity=count_activity,
                evaluate_alliance_military_default=eval_alliance_military_default,
                offset=offset,
            )
        else:
            await funcs.find_targets(
                ctx,
                condition,
                nation,
                count_cities=count_cities,
                count_loot=count_loot,
                count_infrastructure=count_infrastructure,
                count_military=True,
                count_activity=count_activity,
                evaluate_alliance_military_default=eval_alliance_military_default,
                offset=offset,
            )


def setup(bot: Rift):
    bot.add_cog(Targets(bot))
