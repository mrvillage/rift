from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

import discord
from discord.ext import commands

from ... import funcs
from ...cache import cache
from ...data.classes import Nation, Target
from ...ref import Rift


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
    async def target(self, ctx: commands.Context):
        ...

    @target.command(
        name="add",
        brief="Add a target.",
        type=commands.CommandType.chat_input,
        descriptions={
            "nation": "The nation to add.",
            "channels": "The channels to send notifications in.",
            "mentions": "The roles and users to mention when a notification comes.",
            "direct_message": "Whether or not to send a Direct Message as a notification.",
        },
    )
    async def target_add(
        self,
        ctx: commands.Context,
        *,
        nation: Nation,
        channels: List[discord.TextChannel] = [],
        mentions: List[Union[discord.Member, discord.User, discord.Role]] = [],
        direct_message: bool = False,
    ):
        target = await Target.add(
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
                f"Target #{target.id} has been added. It will mention {target.mentions} in {' '.join(i.mention for i in channels)} and will {'' if direct_message else 'not'} Direct Message you when {repr(nation)} comes off beige.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @target.command(
        name="remove",
        brief="Remove a target.",
        type=commands.CommandType.chat_input,
        descriptions={"target": "The target to remove."},
    )
    async def target_remove(self, ctx: commands.Context, *, target: Target):
        await target.remove()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Target #{target.id} has been removed.",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @target.command(
        name="list",
        brief="List all your targets.",
        type=commands.CommandType.chat_input,
    )
    async def target_list(self, ctx: commands.Context):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(
                    f"**#{i.id}**: {repr(i.nation)}"
                    for i in sorted(
                        (i for i in cache.targets if i.owner_id == ctx.author.id),
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
        targets = [i for i in cache.targets if i.nation is after]
        if not targets:
            return
        for target in targets:
            for channel_id in target.channel_ids:
                channel = self.bot.get_channel(channel_id)
                if channel is None:
                    continue
                if TYPE_CHECKING:
                    assert isinstance(channel, discord.TextChannel)
                embed = await after.get_info_embed(TargetContext(self.bot.get_user(target.owner_id), channel.guild))  # type: ignore
                await channel.send(
                    content=f"{repr(after)} is no longer on beige!\n{target.mentions}",
                    embed=embed,
                )
            if target.direct_message:
                owner = self.bot.get_user(target.owner_id)
                if owner is None:
                    continue
                await owner.send(
                    content=f"{repr(after)} is no longer on beige!",
                    embed=await after.get_info_embed(TargetContext(owner, None)),  # type: ignore
                )


def setup(bot: Rift):
    bot.add_cog(Targets(bot))
