from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

import discord
from discord.ext import commands

from ... import funcs
from ...cache import cache
from ...data.classes import Nation, TargetReminder
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
        name="remind",
        brief="A group of commands to manage target reminders",
        type=commands.CommandType.chat_input,
    )
    async def target_remind(self, ctx: RiftContext):
        ...

    @target_remind.command(  # type: ignore
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
    async def target_remind_add(
        self,
        ctx: RiftContext,
        *,
        nation: Nation,
        channels: List[discord.TextChannel] = [],
        mentions: List[Union[discord.Member, discord.User, discord.Role]] = [],
        direct_message: bool = False,
    ):
        reminder = await TargetReminder.add(
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

    @target_remind.command(  # type: ignore
        name="remove",
        brief="Remove a target reminder.",
        type=commands.CommandType.chat_input,
        descriptions={"reminder": "The target reminder to remove."},
    )
    async def target_remind_remove(self, ctx: RiftContext, *, reminder: TargetReminder):
        await reminder.remove()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Target Reminder #{reminder.id} has been removed.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @target_remind.command(  # type: ignore
        name="list",
        brief="List all your target reminders.",
        type=commands.CommandType.chat_input,
    )
    async def target_remind_list(self, ctx: RiftContext):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(
                    f"**#{i.id}**: {repr(i.nation)}"
                    for i in sorted(
                        (
                            i
                            for i in cache.target_reminders
                            if i.owner_id == ctx.author.id
                        ),
                        key=lambda x: x.id,
                    )
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
                embed = await after.get_info_embed(TargetContext(self.bot.get_user(reminder.owner_id), channel.guild))  # type: ignore
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
                    embed=await after.get_info_embed(TargetContext(owner, None)),  # type: ignore
                )


def setup(bot: Rift):
    bot.add_cog(Targets(bot))
